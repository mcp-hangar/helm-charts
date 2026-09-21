{{/*
The process-wide config.yaml sections: tool_access, execution, config_reload,
and the escape hatch for everything else (mcp-hangar/helm-charts#216).

These were unreachable through the chart. The ConfigMap rendered a fixed list
of sections, and none of these was on it, so running the gateway in front_door
mode -- the topology the product is built around -- meant hand-editing the
rendered ConfigMap and having the next `helm upgrade` overwrite it.

Templated rather than passed through, for the reason every other section here
is: a typo fails `helm template` with the key named, instead of becoming an
`unknown_config_key` at boot or a refusal under HANGAR_CONFIG_STRICT. Each key
that a given core is the first to read carries a version guard, so it cannot be
sent to an image that would ignore it.

`extraConfig` is the hatch for sections the chart does not template. It carries
no validation and no version guard, which is exactly why it refuses to write a
section the chart DOES template: two spellings of one setting, with a
precedence rule to remember, is the ambiguity this file exists to remove.
*/}}

{{/* The core image this release resolves to, for the version guards. */}}
{{- define "mcp-hangar.config.coreTag" -}}
{{- .Values.image.tag | default .Chart.AppVersion -}}
{{- end -}}

{{/* Fail when a value needs a core newer than the resolved image tag. Called
     with (list $ "<value>" "<first core that reads it>"). A tag that is not a
     plain version (a digest, a branch build) is left alone: the chart cannot
     order it, and guessing would block a legitimate image. */}}
{{- define "mcp-hangar.config.requireCore" -}}
{{- $root := index . 0 -}}
{{- $what := index . 1 -}}
{{- $min := index . 2 -}}
{{- $tag := include "mcp-hangar.config.coreTag" $root -}}
{{- if and (regexMatch "^[0-9]+\\.[0-9]+\\.[0-9]+" $tag) (semverCompare (printf "< %s-0" $min) $tag) -}}
  {{- fail (printf "\n\n%s needs core %s or newer, and the image resolves to %q.\n\nAn older core does not read the key: it warns, ignores it and runs without the\nsetting, or refuses to start under HANGAR_CONFIG_STRICT. Set image.tag to %s or\nnewer, or leave the value unset.\n" $what $min $tag $min) -}}
{{- end -}}
{{- end -}}

{{/* Every server id this release's mcp_servers builds: the top-level ids, and
     a group member defined only inline in its group, which the loader builds
     from the member's own spec. */}}
{{- define "mcp-hangar.config.knownServerIds" -}}
{{- $ids := list -}}
{{- range $id, $spec := .Values.mcp_servers -}}
  {{- $ids = append $ids $id -}}
  {{- if and (kindIs "map" $spec) (eq (toString (default "" $spec.mode)) "group") -}}
    {{- range $member := ($spec.members | default list) -}}
      {{- if and (kindIs "map" $member) $member.id -}}
        {{- $ids = append $ids (toString $member.id) -}}
      {{- end -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{- $ids | join "," -}}
{{- end -}}

{{/* The `tool_access:` section, or nothing when neither key is set. */}}
{{- define "mcp-hangar.config.toolAccess" -}}
{{- $ta := .Values.toolAccess | default dict -}}
{{- $mode := toString (default "" $ta.mode) -}}
{{- $rc := $ta.requiredCatalogue | default dict -}}
{{- $servers := $rc.servers | default list -}}
{{- if and $mode (not (has $mode (list "egress" "front_door"))) -}}
  {{- fail (printf "\n\ntoolAccess.mode is %q; it must be \"egress\" or \"front_door\".\n\nCore refuses an unrecognised mode at startup rather than falling back to\negress -- quietly resolving a typo would hand you the permissive topology\nwhile the config says otherwise -- so this would be a gateway that does not\nstart.\n" $mode) -}}
{{- end -}}
{{- if $servers -}}
  {{- include "mcp-hangar.config.requireCore" (list . "toolAccess.requiredCatalogue" "2.21.0") -}}
  {{- $known := splitList "," (include "mcp-hangar.config.knownServerIds" .) -}}
  {{- range $name := $servers -}}
    {{- if not (has (toString $name) $known) -}}
      {{- fail (printf "\n\ntoolAccess.requiredCatalogue.servers names %q, which this release's\nmcp_servers does not build.\n\nCore refuses a required catalogue naming something it cannot project, so this\nwould be a gateway that does not start. Known ids: %s\n" $name (join ", " $known)) -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{- if or $mode $servers -}}
tool_access:
  {{- with $mode }}
  mode: {{ . }}
  {{- end }}
  {{- if $servers }}
  required_catalogue:
    servers:
      {{- range $servers }}
      - {{ . | quote }}
      {{- end }}
    {{- with $rc.retryForSeconds }}
    retry_for_s: {{ . }}
    {{- end }}
  {{- end }}
{{- end -}}
{{- end -}}

{{/* The `execution:` section, or nothing when no key is set. */}}
{{- define "mcp-hangar.config.execution" -}}
{{- $e := .Values.execution | default dict -}}
{{- $tenants := $e.tenantLimits | default dict -}}
{{- if $tenants -}}
  {{- include "mcp-hangar.config.requireCore" (list . "execution.tenantLimits" "2.21.0") -}}
  {{- range $tenant, $budget := $tenants -}}
    {{- if not (and (kindIs "map" $budget) $budget.maxConcurrency $budget.rps $budget.burst) -}}
      {{- fail (printf "\n\nexecution.tenantLimits.%s must set maxConcurrency, rps and burst.\n\nCore requires all three on every entry and refuses the file otherwise: a\nbudget with one of them missing is not a smaller budget, it is a gateway that\ndoes not start.\n" $tenant) -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{- if or $tenants (not (kindIs "invalid" $e.defaultMcpServerConcurrency)) (not (kindIs "invalid" $e.maxConcurrency)) -}}
execution:
  {{- with $e.defaultMcpServerConcurrency }}
  default_mcp_server_concurrency: {{ . }}
  {{- end }}
  {{- with $e.maxConcurrency }}
  max_concurrency: {{ . }}
  {{- end }}
  {{- if $tenants }}
  tenant_limits:
    {{- range $tenant, $budget := $tenants }}
    {{ $tenant | quote }}:
      max_concurrency: {{ $budget.maxConcurrency }}
      rps: {{ $budget.rps }}
      burst: {{ $budget.burst }}
    {{- end }}
  {{- end }}
{{- end -}}
{{- end -}}

{{/* The `config_reload:` section, or nothing when no key is set. */}}
{{- define "mcp-hangar.config.configReload" -}}
{{- $r := .Values.configReload | default dict -}}
{{- if or (not (kindIs "invalid" $r.enabled)) (not (kindIs "invalid" $r.intervalSeconds)) (not (kindIs "invalid" $r.useWatchdog)) -}}
config_reload:
  {{- if not (kindIs "invalid" $r.enabled) }}
  enabled: {{ $r.enabled }}
  {{- end }}
  {{- with $r.intervalSeconds }}
  interval_s: {{ . }}
  {{- end }}
  {{- if not (kindIs "invalid" $r.useWatchdog) }}
  use_watchdog: {{ $r.useWatchdog }}
  {{- end }}
{{- end -}}
{{- end -}}

{{/* Sections the chart templates. extraConfig may not write any of them: the
     chart's copy has the validation and the version guard, and two spellings
     of one setting would need a precedence rule nobody would remember. */}}
{{- define "mcp-hangar.config.templatedSections" -}}
auth,config_reload,coordination,execution,http,logging,mcp_servers,persistence,tool_access,truncation
{{- end -}}

{{/* `extraConfig`, checked and rendered. */}}
{{- define "mcp-hangar.config.extra" -}}
{{- $extra := .Values.extraConfig | default dict -}}
{{- if $extra -}}
  {{- $templated := splitList "," (include "mcp-hangar.config.templatedSections" .) -}}
  {{- range $section, $_ := $extra -}}
    {{- if has (toString $section) $templated -}}
      {{- fail (printf "\n\nextraConfig sets %q, which this chart templates itself.\n\nThe chart's own value for that section is checked at render time and carries a\nversion guard; extraConfig carries neither, and having both would need a\nprecedence rule to remember. Move the setting to the chart value for %s and\nleave extraConfig for sections the chart does not template.\n" $section $section) -}}
    {{- end -}}
  {{- end -}}
{{- toYaml $extra -}}
{{- end -}}
{{- end -}}

{{/* Keys core removed in 2.20.0, which render as unknown keys nothing reads.
     `tool_access.rules` cannot be set at all any more -- the chart has no value
     for it -- but `mcp_servers` is a passthrough, so a group's reset timeout
     can still be written there and would be refused at boot. */}}
{{- define "mcp-hangar.config.refuseRemovedKeys" -}}
{{- range $id, $spec := .Values.mcp_servers -}}
  {{- if kindIs "map" $spec -}}
    {{- $found := "" -}}
    {{- if hasKey $spec "circuit_reset_timeout_s" -}}
      {{- $found = "circuit_reset_timeout_s" -}}
    {{- else if and (kindIs "map" $spec.circuit_breaker) (hasKey $spec.circuit_breaker "reset_timeout_s") -}}
      {{- $found = "circuit_breaker.reset_timeout_s" -}}
    {{- end -}}
    {{- if $found -}}
      {{- fail (printf "\n\nmcp_servers.%s sets %s, which core removed in 2.20.0.\n\nA group's circuit closes once `min_healthy` members are back in rotation,\nnever on a timer, so the key never had a reader. Core refuses it under\nHANGAR_CONFIG_STRICT and warns otherwise. Delete it.\n" $id $found) -}}
    {{- end -}}
  {{- end -}}
{{- end -}}
{{- end -}}
