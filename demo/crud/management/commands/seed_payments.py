from django.core.management.base import BaseCommand
from datetime import date, timedelta
from crud.models import PayoutCycle, CompensationRecovery


class Command(BaseCommand):
    help = "Seed sample Payout Cycle and Compensation/Recovery data for the Payments dashboard"

    def handle(self, *args, **options):
        PayoutCycle.objects.all().delete()
        CompensationRecovery.objects.all().delete()

        PayoutCycle.objects.create(
            cycle_date=date(2026, 8, 13),
            status="upcoming",
            sales_returns=-315,
            ads_cost=0,
            program_cost=0,
            program_benefits=0,
            referral_earnings=0,
        )

        completed_data = [
            (date(2026, 2, 10), 951.16, "AXISCN1247519098"),
            (date(2026, 2, 4), 1020.00, "AXISCN1247519099"),
            (date(2026, 2, 3), 696.78, "AXISCN1247519100"),
        ]
        for cycle_date, amount, neft in completed_data:
            PayoutCycle.objects.create(
                cycle_date=cycle_date,
                status="completed",
                sales_returns=amount,
                ads_cost=0,
                program_cost=0,
                program_benefits=0,
                referral_earnings=0,
                neft_id=neft,
            )

        CompensationRecovery.objects.create(
            record_type="compensation", amount=0, description="Sample compensation", date=date(2026, 2, 1)
        )
        CompensationRecovery.objects.create(
            record_type="recovery", amount=0, description="Sample recovery", date=date(2026, 2, 1)
        )

        self.stdout.write(self.style.SUCCESS("Sample payments data seeded successfully."))