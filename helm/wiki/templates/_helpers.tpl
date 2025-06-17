{{/*
Helper templates for the Helm chart
*/}}

{{- define "wiki.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "wiki.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}

{{- define "wiki.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "wiki.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
{{- .Release.Name }}-{{ .Chart.Name }}-sa
{{- else -}}
{{- .Values.serviceAccount.name | quote }}
{{- end -}}
{{- end -}}

{{- define "wiki.labels" -}}
app: {{ .Chart.Name }}
release: {{ .Release.Name }}
{{- end -}}

{{- define "wiki.selectorLabels" -}}
{{- include "wiki.labels" . | nindent 4 }}
{{- end -}}