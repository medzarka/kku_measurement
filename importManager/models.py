from django.db import models


class UploadDocument(models.Model):
    upload_document_id = models.AutoField(primary_key=True, verbose_name="Upload Document ID")
    upload_document_description = models.CharField(max_length=255, blank=True, verbose_name="Upload Document "
                                                                                            "Description")
    upload_document_document = models.FileField(upload_to='documents/upload', verbose_name="Upload Document Path")
    upload_document_uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Upload Document Time")

    def __str__(self):
        return self.upload_document_document.url

    class Meta:
        ordering = ['upload_document_uploaded_at', 'upload_document_document', ]
        verbose_name_plural = "Upload Documents"
        verbose_name = "Upload Document"
        indexes = [
            models.Index(fields=['upload_document_document', ]),
            models.Index(fields=['upload_document_uploaded_at', ]),
        ]


class GeneratedDocument(models.Model):
    generated_document_id = models.AutoField(primary_key=True, verbose_name="Generated Document ID")
    generated_document_description = models.CharField(max_length=255, blank=True, verbose_name='Generated Document '
                                                                                               'Description')
    generated_document_document = models.FileField(upload_to='documents/generated', verbose_name='Generated Document Path')
    generated_document_generated_at = models.DateTimeField(auto_now_add=True, verbose_name='Generated Document Time')

    def __str__(self):
        return self.generated_document_document.url

    class Meta:
        ordering = ['generated_document_generated_at', 'generated_document_document', ]
        verbose_name_plural = "Generated Documents"
        verbose_name = "Generated Document"
        indexes = [
            models.Index(fields=['generated_document_document', ]),
            models.Index(fields=['generated_document_generated_at', ]),
        ]


class Translation(models.Model):
    translation_id = models.AutoField(primary_key=True, verbose_name="Section ID")
    translation_ar = models.CharField(max_length=500, unique=True, verbose_name="Translation AR")
    translation_en = models.CharField(max_length=500, verbose_name="Translation EN", null=True,
                                      blank=True)

    def __str__(self):
        return self.translation_ar

    class Meta:
        ordering = ['translation_ar', ]
        verbose_name_plural = "Translations"
        verbose_name = "Translation"
        indexes = [
            models.Index(fields=['translation_ar', ]),
            models.Index(fields=['translation_en', ]),
        ]
