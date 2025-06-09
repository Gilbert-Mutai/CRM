import random
from faker import Faker
from django.contrib.auth import get_user_model
from core.models import Client
from threecx.models import ThreeCX

fake = Faker()
User = get_user_model()
users = list(User.objects.all())

def generate_company_clients(num=50):
    clients = []

    for _ in range(num):
        client = Client(
            client_type=Client.COMPANY,
            name=fake.company(),
            contact_person=fake.name(),
            email=fake.unique.email(),
            phone_number='+' + ''.join(filter(str.isdigit, fake.phone_number()))[:15],
            created_by=random.choice(users) if users else None,
            updated_by=random.choice(users) if users else None,
        )
        try:
            client.full_clean()
            client.save()
            clients.append(client)
        except Exception as e:
            print(f"[COMPANY] Skipping client due to validation error: {e}")

    return clients

def generate_threecx_records(clients, num=50):
    sip_providers = [choice[0] for choice in ThreeCX.SIP_PROVIDERS]
    license_types = [choice[0] for choice in ThreeCX.LICENSE_TYPES]
    fqdn_set = set()

    for _ in range(num):
        client = random.choice(clients)
        sip_provider = random.choice(sip_providers)
        license_type = random.choice(license_types)

        while True:
            fqdn = fake.domain_name()
            if fqdn not in fqdn_set:
                fqdn_set.add(fqdn)
                break

        threecx = ThreeCX(
            client=client,
            sip_provider=sip_provider,
            fqdn=fqdn,
            license_type=license_type,
            created_by=random.choice(users) if users else None,
            updated_by=random.choice(users) if users else None,
        )
        try:
            threecx.full_clean()
            threecx.save()
        except Exception as e:
            print(f"[3CX] Skipping record due to validation error: {e}")

# Run the script
clients = generate_company_clients(50)
generate_threecx_records(clients, 50)
print("✅ Done populating sample data for COMPANY clients.")
