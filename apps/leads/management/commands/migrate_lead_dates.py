from django.core.management.base import BaseCommand
from apps.leads.models import Lead, FollowUp

class Command(BaseCommand):
    help = 'Migrate last_contact_date and return_contact from Lead to FollowUp'

    def handle(self, *args, **kwargs):
        leads = Lead.objects.all()
        for lead in leads:
            if lead.last_contact_date or lead.return_contact:
                FollowUp.objects.create(
                    lead=lead,
                    last_contact_date=lead.last_contact_date,
                    return_contact=lead.return_contact if lead.return_contact else None
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully migrated dates for lead {lead.id}'))

        self.stdout.write(self.style.SUCCESS('Migration completed successfully.'))
