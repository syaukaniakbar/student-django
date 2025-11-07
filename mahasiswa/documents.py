# mahasiswa/documents.py
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Mahasiswa

@registry.register_document
class MahasiswaDocument(Document):
    class Index:
        name = 'mahasiswa'  # nama index di Elasticsearch
    
    class Django:
        model = Mahasiswa
        fields = [
            'id',  # tambahkan field ID
            'nim',
            'nama_lengkap',
            'jurusan',
            'fakultas',
            'kota',
            'email',
            'angkatan',
            'ipk',
            'status',
        ]
