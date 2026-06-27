{{- define "companyos.name" -}}
{{- default "companyos" .Values.nameOverride -}}
{{- end -}}

{{- define "companyos.databaseUrl" -}}
{{- if .Values.externalDatabaseUrl -}}
{{- .Values.externalDatabaseUrl -}}
{{- else -}}
postgresql+asyncpg://companyos:companyos@{{ include "companyos.name" . }}-postgres:5432/companyos
{{- end -}}
{{- end -}}
