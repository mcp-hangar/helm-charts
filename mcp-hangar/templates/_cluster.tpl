{{/*
The combinations that fail *after* deployment rather than during it.

Every rule here is one core already enforces at startup. Catching them at
render time is not duplication for its own sake: the failure they prevent is a
pod that starts, passes its probes and disagrees with its peers, or a
CrashLoopBackOff whose reason is three `kubectl logs` away. `helm install`
refusing with the reason is the cheaper place to learn it.

The one rule core cannot enforce is the first: it never sees `replicaCount`.
*/}}
{{- define "mcp-hangar.validateCluster" -}}
{{- $p := .Values.persistence | default dict -}}
{{- $backend := $p.backend | default "" -}}
{{- $coord := .Values.coordination | default dict -}}

{{/* The most replicas this release can run, not the ones it starts with: an
     autoscaler that can reach 2 is a cluster that has not happened yet. */}}
{{- $maxReplicas := int .Values.replicaCount -}}
{{- if and .Values.autoscaling .Values.autoscaling.enabled -}}
{{- $maxReplicas = int .Values.autoscaling.maxReplicas -}}
{{- end -}}

{{- if gt $maxReplicas 1 -}}
  {{- if ne $backend "postgresql" -}}
    {{- fail (printf "\n\nreplicaCount/autoscaling allows %d replicas, but persistence.backend is %q.\n\nReplicas that cannot share storage are not one gateway: each would get its own\nfile, grant itself its own lease, run its own management loops and hold its own\nfleet. They never disagree, because they cannot see each other -- every probe\nstays green while the deployment has as many fleets as it has pods.\n\nSet persistence.backend=postgresql with a host every replica can reach, or keep\nreplicaCount=1.\n" $maxReplicas $backend) -}}
  {{- end -}}
  {{- if not $coord.enabled -}}
    {{- fail (printf "\n\nreplicaCount/autoscaling allows %d replicas, but coordination.enabled is false.\n\nWithout it these are several independent gateways sharing a database rather\nthan one gateway with replicas. Set coordination.enabled=true.\n" $maxReplicas) -}}
  {{- end -}}
{{- end -}}

{{- if and $coord.enabled (ne $backend "postgresql") -}}
  {{- fail (printf "\n\ncoordination.enabled is true and persistence.backend is %q.\n\nThe gateway refuses to start in this combination: a coordination block is the\nstatement that these replicas are one gateway, and that requires storage they\ncan share. Use postgresql, or turn coordination off.\n" $backend) -}}
{{- end -}}

{{- if $coord.enabled -}}
  {{- if ge (float64 $coord.renewDeadlineSeconds) (float64 $coord.leaseTtlSeconds) -}}
    {{- fail (printf "\n\ncoordination.renewDeadlineSeconds (%v) must be under leaseTtlSeconds (%v).\n\nThe gap is what keeps two managers from overlapping: an instance gives the\nlease up on its own before the tenure it wrote can expire, so it stops slightly\nearly rather than slightly late.\n" $coord.renewDeadlineSeconds $coord.leaseTtlSeconds) -}}
  {{- end -}}
  {{- range $id, $spec := .Values.mcp_servers -}}
    {{- $mode := lower (toString (default "" $spec.mode)) -}}
    {{- if has $mode (list "subprocess" "docker" "container") -}}
      {{- fail (printf "\n\nmcp_servers.%s uses mode %q in a coordinated deployment.\n\nThat mode runs the server as a child process of ONE gateway: no peer has an\naddress for it, so only the replica holding the management lease can serve it\nand the others answer as though it had no tools. The gateway refuses to start\nwith this configuration.\n\nUse mode: remote, or turn coordination off.\n" $id $mode) -}}
    {{- end -}}
  {{- end -}}
{{- end -}}

{{/* These keys are inert on a core that predates them: 2.4.0 does not know
     `persistence` or `coordination`, so it would ignore both and run its old
     per-subsystem storage while the operator believed a backend was selected.
     Silently getting the old behaviour is the failure mode this whole release
     exists to remove, so it is refused instead.

     appVersion deliberately tracks the last STABLE core, not the newest tag: a
     chart whose default is a release candidate hands one to everybody who runs
     `helm install`. Using these keys before 2.5.0 is stable therefore means
     naming the image yourself. */}}
{{- $tag := .Values.image.tag | default .Chart.AppVersion -}}
{{- if or (ne $backend "") $coord.enabled -}}
  {{- if and (regexMatch "^[0-9]+\\.[0-9]+\\.[0-9]+" $tag) (semverCompare "< 2.5.0-0" $tag) -}}
    {{- fail (printf "\n\npersistence/coordination need core 2.5.0 or newer, and the image resolves to %q.\n\nOn an older core both blocks are ignored: it would run its previous\nper-subsystem storage while you believed a backend was selected.\n\nSet image.tag to 2.5.0 or newer (or a candidate, e.g. 2.5.0-rc.2, while 2.5.0\nis unreleased).\n" $tag) -}}
  {{- end -}}
{{- end -}}

{{- if and (eq $backend "postgresql") (not $p.postgresql.host) -}}
  {{- fail "\n\npersistence.backend is postgresql but persistence.postgresql.host is empty.\n" -}}
{{- end -}}
{{- end -}}
