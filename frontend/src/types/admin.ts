export interface AdminOverviewStats {
  total_users: number;
  banned_users: number;
  admin_users: number;
  total_opportunities: number;
  open_opportunities: number;
  total_groups: number;
  total_audit_logs: number;
}

export interface AuditLogItem {
  id: string;
  user_id?: string;
  user_email?: string;
  action: string;
  details: string;
  ip_address: string;
  timestamp: string;
}
