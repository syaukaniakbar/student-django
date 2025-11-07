from django_elasticsearch_dsl.registries import registry
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Mahasiswa
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Mahasiswa)
def update_document(sender, instance, **kwargs):
    try:
        registry.update(instance)
    except Exception as e:
        logger.error(f"Error updating Elasticsearch document for Mahasiswa {instance.pk}: {str(e)}")

@receiver(post_delete, sender=Mahasiswa)
def delete_document(sender, instance, **kwargs):
    try:
        registry.delete(instance)
    except Exception as e:
        logger.error(f"Error deleting Elasticsearch document for Mahasiswa {instance.pk}: {str(e)}")
