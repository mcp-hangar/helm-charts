{{/*
Expand the name of the chart.
*/}}
{{- define "mcp-hangar-operator.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "mcp-hangar-operator.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "mcp-hangar-operator.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mcp-hangar-operator.labels" -}}
helm.sh/chart: {{ include "mcp-hangar-operator.chart" . }}
{{ include "mcp-hangar-operator.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: mcp-hangar
{{- end }}

{{/*
Selector labels
*/}}
{{- define "mcp-hangar-operator.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mcp-hangar-operator.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: operator
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "mcp-hangar-operator.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "mcp-hangar-operator.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Create the name of the credentials secret
*/}}
{{- define "mcp-hangar-operator.credentialsSecretName" -}}
{{- if .Values.hangar.existingSecret }}
{{- .Values.hangar.existingSecret }}
{{- else }}
{{- include "mcp-hangar-operator.fullname" . }}-credentials
{{- end }}
{{- end }}

{{/*
Whether webhook infrastructure (cert, service, volume mounts) is needed.
True when admission webhooks are enabled. (The CRD conversion knob went with
v1alpha1 -- operator 0.16.0 serves a single version and has no /convert.)
*/}}
{{- define "mcp-hangar-operator.webhookEnabled" -}}
{{- if .Values.webhook.enabled -}}
true
{{- end -}}
{{- end }}
