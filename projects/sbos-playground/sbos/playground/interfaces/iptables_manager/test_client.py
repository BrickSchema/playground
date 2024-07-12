import iptables_manager

# iptables_manager.create_chain("chishi")
# iptables_manager.grant_external_access("chishi","172.25.0.2","tcp","47.254.124.205")
# iptables_manager.grant_host_access("chishi","172.25.0.2","tcp")
# iptables_manager.revoke_external_access("chishi","172.25.0.2","tcp","47.254.124.205")
# iptables_manager.revoke_host_access("chishi","172.25.0.2","tcp")
# iptables_manager.revoke_all_access("chishi",1)
iptables_manager.delete_chain("chishi")
