{{- define "hangar-cloud.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "hangar-cloud.fullname" -}}
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

{{- define "hangar-cloud.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "hangar-cloud.labels" -}}
helm.sh/chart: {{ include "hangar-cloud.chart" . }}
{{ include "hangar-cloud.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "hangar-cloud.selectorLabels" -}}
app.kubernetes.io/name: {{ include "hangar-cloud.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "hangar-cloud.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "hangar-cloud.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/* Database URL helper -- uses built-in postgresql sub-chart or external */}}
{{- define "hangar-cloud.databaseURL" -}}
{{- if .Values.postgresql.enabled }}
{{- $host := printf "%s-postgresql" .Release.Name }}
{{- $user := .Values.postgresql.auth.username }}
{{- $db := .Values.postgresql.auth.database }}
{{- printf "postgres://%s:$(POSTGRES_PASSWORD)@%s:5432/%s?sslmode=disable" $user $host $db }}
{{- else if .Values.externalDatabase.url }}
{{- .Values.externalDatabase.url }}
{{- else }}
{{- $host := required "externalDatabase.host is required when postgresql.enabled=false" .Values.externalDatabase.host }}
{{- $user := required "externalDatabase.username is required when postgresql.enabled=false" .Values.externalDatabase.username }}
{{- $db := .Values.externalDatabase.database }}
{{- $port := .Values.externalDatabase.port | int }}
{{- $ssl := .Values.externalDatabase.sslmode }}
{{- printf "postgres://%s:$(POSTGRES_PASSWORD)@%s:%d/%s?sslmode=%s" $user $host $port $db $ssl }}
{{- end }}
{{- end }}

{{/* Database password secret name */}}
{{- define "hangar-cloud.databaseSecretName" -}}
{{- if .Values.postgresql.enabled }}
{{- printf "%s-postgresql" .Release.Name }}
{{- else if .Values.externalDatabase.existingSecret }}
{{- .Values.externalDatabase.existingSecret }}
{{- else }}
{{- include "hangar-cloud.fullname" . }}-db-credentials
{{- end }}
{{- end }}

{{/* Database password secret key */}}
{{- define "hangar-cloud.databaseSecretKey" -}}
{{- if .Values.postgresql.enabled }}
{{- "password" }}
{{- else }}
{{- .Values.externalDatabase.secretKey | default "password" }}
{{- end }}
{{- end }}

{{/* Redis address helper */}}
{{- define "hangar-cloud.redisAddr" -}}
{{- if .Values.redis.enabled }}
{{- printf "%s-redis-master:6379" .Release.Name }}
{{- else }}
{{- required "externalRedis.addr is required when redis.enabled=false" .Values.externalRedis.addr }}
{{- end }}
{{- end }}

{{/* Redis password secret name (empty if no auth) */}}
{{- define "hangar-cloud.redisPasswordSecretName" -}}
{{- if and (not .Values.redis.enabled) .Values.externalRedis.existingSecret }}
{{- .Values.externalRedis.existingSecret }}
{{- end }}
{{- end }}

