export interface GroupMemberRead {
  id: string;
  user_id: string;
  name: string;
  email: string;
  can_create: boolean;
  can_edit: boolean;
  can_assign: boolean;
  is_owner: boolean;
  joined_at: string;
}

export interface GroupRead {
  id: string;
  name: string;
  description: string;
  owner_id: string;
  owner_name?: string;
  created_at: string;
  members_count: number;
  members?: GroupMemberRead[];
}

export interface GroupCreateInput {
  name: string;
  description: string;
}

export interface GroupMemberAddInput {
  email: string;
  can_create: boolean;
  can_edit: boolean;
  can_assign: boolean;
}
