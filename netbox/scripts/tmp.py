def run (self, data, commit):
    site = data['site']
    site_no = data['site_no']
    rack_name = data['rack_name']
    rack_units = data['rack_units'] 
    panel_ports = data['panel_ports']
    pole_setup = data['pole_setup']
    sw_asset_tag = data['sw_asset_tag']
    bbr_asset_tag = data['bbr_asset_tag']
    node_id = data['node_id']

    # Set up POP Mgmt VLAN
    vlan = self.create_mgmt_vlan (site, site_no)

    # Mgmt prefix
    prefix = self.create_mgmt_prefix (site, site_no, vlan)

    # Create rack
    rack = self.create_rack (site, rack_name, rack_units)

    # Create patch panel
    pp = self.create_patch_panel (site, rack, rack_name, panel_ports)

    self.create_and_connect_surges (site, rack, pp, pole_setup)

    # Create switch
    sw = self.setup_swtich (site, rack, pp, panel_ports, vlan, site_no, sw_asset_tag)

    # Create backbone router
    bbr = self.setup_bbr (site, rack, vlan, site_no, node_id, bbr_asset_tag, sw)

    
def create_mgmt_vlan (self, site, site_no):
    vlan_id = 3000 + int (site_no)
    try:
        vlan = VLAN.objects.get (site = site, vid = vlan_id)                  
        self.log_info ("Mgmt vlan %s already present, carrying on." % vlan)
        return vlan
    except VLAN.DoesNotExist:
        pass

    vlan = VLAN (
        site = site,
        name = "Mgmt %s" % site.name,
        vid = vlan_id,
        role = Role.objects.get (name = 'Mgmt')
    )

    vlan.save ()
    self.log_success ("Created mgmt VLAN %s" % vlan)

    return vlan


def create_mgmt_prefix (self, site, site_no, vlan):
    prefix_cidr = "172.30.%d.0/24" % site_no
    try:
        prefix = Prefix.objects.get (prefix = prefix_cidr)
        self.log_info ("Mgmt prefix %s already present, carrying on." % prefix)

        return prefix
    except Prefix.DoesNotExist:
        pass

    prefix = Prefix (
        site = site,
        prefix = prefix_cidr,
        vlan = vlan,
        role = Role.objects.get (name = 'Mgmt')
    )

    prefix.save ()
    self.log_success ("Created mgmt prefix %s" % prefix)

    return prefix
