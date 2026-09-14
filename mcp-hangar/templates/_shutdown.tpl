{{/*
Pod shutdown (mcp-hangar/mcp-hangar#1447): the preStop sleep, core's HTTP
graceful-shutdown bound, and the grace period that has to hold both.

The kubelet starts the grace period when it runs the preStop hook, and sends
SIGTERM only when the hook returns. After SIGTERM core waits up to the bound for
the requests in flight, then stops its servers and releases its lease. So a pod
needs

    terminationGracePeriodSeconds > preStopSleepSeconds + gracefulTimeoutSeconds

or the SIGKILL at the end of the grace period cuts off the requests the bound
was set to wait for. That is what a 90 s bound under Kubernetes' default 30 s
grace period did. The render fails instead of shipping it.
*/}}

{{/* What a computed grace period adds after preStop + bound, for core's own
     cleanup once the requests are done. */}}
{{- define "mcp-hangar.shutdown.cleanupSeconds" -}}10{{- end -}}

{{/* Kubernetes' own grace period, in force when the chart renders none. */}}
{{- define "mcp-hangar.shutdown.kubernetesDefaultGraceSeconds" -}}30{{- end -}}

{{/* A value in whole seconds, at least <min>, or a failed render naming it.
     Null renders nothing. Called with (list "<name>" <value> <min>). */}}
{{- define "mcp-hangar.shutdown.seconds" -}}
{{- $name := index . 0 -}}
{{- $v := index . 1 -}}
{{- $min := index . 2 -}}
{{- if not (kindIs "invalid" $v) -}}
  {{- $number := or (kindIs "float64" $v) (kindIs "int64" $v) (kindIs "int" $v) -}}
  {{- if or (not $number) (ne (float64 $v) (float64 (int64 $v))) (lt (int64 $v) (int64 $min)) -}}
    {{- fail (printf "\n\n%s is %v; it must be a whole number of seconds, %d or more.\n" $name $v $min) -}}
  {{- end -}}
  {{- int64 $v -}}
{{- end -}}
{{- end -}}

{{/* shutdown.gracefulTimeoutSeconds, checked. Empty when unset. */}}
{{- define "mcp-hangar.shutdown.gracefulTimeoutSeconds" -}}
{{- $s := .Values.shutdown | default dict -}}
{{- $bound := include "mcp-hangar.shutdown.seconds" (list "shutdown.gracefulTimeoutSeconds" $s.gracefulTimeoutSeconds 1) -}}
{{- if $bound -}}
  {{- /* An older core does not know the key. It warns and ignores it, so it
         waits without a bound while the grace period is sized for one, and
         under HANGAR_CONFIG_STRICT it refuses to start. Refused here instead,
         as the persistence/coordination keys are in _cluster.tpl. */ -}}
  {{- $tag := .Values.image.tag | default .Chart.AppVersion -}}
  {{- if and (regexMatch "^[0-9]+\\.[0-9]+\\.[0-9]+" $tag) (semverCompare "< 2.20.0-0" $tag) -}}
    {{- fail (printf "\n\nshutdown.gracefulTimeoutSeconds needs core 2.20.0 or newer, and the image resolves to %q.\n\nAn older core does not read http.graceful_shutdown_timeout_s: it warns, ignores\nit and waits without a bound, or refuses to start under HANGAR_CONFIG_STRICT.\n\nSet image.tag to 2.20.0 or newer, or leave shutdown.gracefulTimeoutSeconds unset.\n" $tag) -}}
  {{- end -}}
{{- end -}}
{{- $bound -}}
{{- end -}}

{{/* shutdown.preStopSleepSeconds, checked. "0" when unset. */}}
{{- define "mcp-hangar.shutdown.preStopSleepSeconds" -}}
{{- $s := .Values.shutdown | default dict -}}
{{- include "mcp-hangar.shutdown.seconds" (list "shutdown.preStopSleepSeconds" $s.preStopSleepSeconds 0) | default "0" -}}
{{- end -}}

{{/* The grace period to render, or empty to leave Kubernetes' default in force.

     Set: rendered as given. Unset with a bound: preStop + bound + cleanup.
     Unset without one: not rendered, so an install that sets no bound keeps
     Kubernetes' default. Whichever is in force -- set, computed or the default
     -- the render fails unless it is longer than preStop + bound. */}}
{{- define "mcp-hangar.shutdown.terminationGracePeriodSeconds" -}}
{{- $s := .Values.shutdown | default dict -}}
{{- $bound := include "mcp-hangar.shutdown.gracefulTimeoutSeconds" . -}}
{{- $sleep := include "mcp-hangar.shutdown.preStopSleepSeconds" . | atoi -}}
{{- $set := include "mcp-hangar.shutdown.seconds" (list "shutdown.terminationGracePeriodSeconds" $s.terminationGracePeriodSeconds 1) -}}
{{- $cleanup := include "mcp-hangar.shutdown.cleanupSeconds" . | atoi -}}
{{- $needs := add $sleep (atoi (default "0" $bound)) -}}
{{- $grace := include "mcp-hangar.shutdown.kubernetesDefaultGraceSeconds" . | atoi -}}
{{- $from := "Kubernetes' default" -}}
{{- if $set -}}
  {{- $grace = atoi $set -}}
  {{- $from = "shutdown.terminationGracePeriodSeconds" -}}
{{- else if $bound -}}
  {{- $grace = add $needs $cleanup -}}
  {{- $from = "computed" -}}
{{- end -}}
{{- if le (int64 $grace) (int64 $needs) -}}
  {{- fail (printf "\n\nThe pod's grace period (%d s, %s) must be longer than\nshutdown.preStopSleepSeconds (%d s) + shutdown.gracefulTimeoutSeconds (%s) = %d s.\n\nThe kubelet counts the grace period from the start of the preStop hook and\nkills the pod when it ends, so a shorter one cuts off the requests core is\nstill waiting for.\n\nRaise shutdown.terminationGracePeriodSeconds, or leave it unset and set\nshutdown.gracefulTimeoutSeconds, so the chart computes preStop + bound + %d s.\n" (int64 $grace) $from $sleep (default "unset" $bound) (int64 $needs) $cleanup) -}}
{{- end -}}
{{- if or $set $bound -}}
{{- int64 $grace -}}
{{- end -}}
{{- end -}}
