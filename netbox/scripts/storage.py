# Скрипт для добавления устройств на склад

from django.utils.text import slugify

from dcim.choices import DeviceStatusChoices, SiteStatusChoices
from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from extras.scripts import *
import json
import jsonschema

name = 'Хранилище'
storage = Site.objects.get(slug='bel-store')

        
def validate_device(device):
    device_schema = {
        "type": "object",
        "properties": {
            "device_role": { "type": "string"},
            "manufacturer": { "type": "string"},
            "device_type": { "type": "string"},

            "serial": { "type": "string"},
            "asset_tag": { "type": "sting"}
        }
    }        
    try:
        device = Device.objects.get( serial = serial )
        return True
    except Device.DoesNotExist:
        return False


class StoreDevice(Script):

    class Meta:
        name = "Добавить устройство"
        description = "Добавление на склад устройства"
        commit_default = False
        field_order = ['manufacturer', 'device_type', 'device_role', 'json']
    
    manufacturer = ObjectVar(
        model = Manufacturer,
        required = True
    )

    device_type = ObjectVar(
        model = DeviceType,
        required = True,
        display_field = 'model',
        query_params = {
            'manufacturer_id': '$manufacturer'
        }
    )

    device_role = ObjectVar(
        model = DeviceRole,
        required = True,
        display_field = 'model',
        query_params = {
            'slug__ic': '$device_type.slug'
        }

    )

    json = FileVar(
        description = "JSON с данными устройств для добавление в хранилище"
    )

    def run(self, data, commit):
        self.log_success(f"Найдено хранилище:  [{storage.name}](/dcim/sites/{storage.slug})")
        try:
            devices = json.load(data['json'])
        except ValueError as err:
            self.log_failure(f"Ошибка входных данных\n{err}")
            return False

        return 'OK'

        # for device in devices:



class StoreInventory(Script):

    class Meta:
        name = "Добавить инвентарь"
        description = "Добавление на склад инвентаря"
        commit_default = False
        # field_order = ['site_name', 'switch_count', 'switch_model']

    # site_name = StringVar(
    #     description="Name of the new site"
    # )
    # switch_count = IntegerVar(
    #     description="Number of access switches to create"
    # )
    # manufacturer = ObjectVar(
    #     model=Manufacturer,
    #     required=False
    # )
    # switch_model = ObjectVar(
    #     description="Access switch model",
    #     model=DeviceType,
    #     display_field='model',
    #     query_params={
    #         'manufacturer_id': '$manufacturer'
    #     }
    # )

    def run(self, data, commit):

        # Create the new site
        #  (
        #     # name=data['site_name'],
        #     slug=slugify(data['site_name']),
        #     status=SiteStatusChoices.STATUS_PLANNED
        # )
        # site.save()
        self.log_success(f"Найдено хранилище: {storage}")

        # Create access switches
        # switch_role = DeviceRole.objects.get(name='Access Switch')
        # for i in range(1, data['switch_count'] + 1):
        #     switch = Device(
        #         device_type=data['switch_model'],
        #         name=f'{site.slug}-switch{i}',
        #         site=site,
        #         status=DeviceStatusChoices.STATUS_PLANNED,
        #         device_role=switch_role
        #     )
        #     switch.save()
        #     self.log_success(f"Created new switch: {switch}")

        # Generate a CSV table of new devices
        # output = [
        #     'name,make,model'
        # ]
        # for switch in Device.objects.filter(site=site):
        #     attrs = [
        #         switch.name,
        #         switch.device_type.manufacturer.name,
        #         switch.device_type.model
        #     ]
        #     output.append(','.join(attrs))

        # return '\n'.join(output)

