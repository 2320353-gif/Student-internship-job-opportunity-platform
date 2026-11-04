export interface Internship {
  id: string;
  title: string;
  company_name: string;
  location: string;
  description: string;
  salary: string;
  deadline: string;
  status: "Open" | "Closed" | string;
  created_at: string;
}

export interface InternshipCreateInput {
  title: string;
  company_name: string;
  location: string;
  description: string;
  salary: string;
  deadline: string;
  status: "Open" | "Closed" | string;
}

export interface InternshipUpdateInput {
  title?: string;
  company_name?: string;
  location?: string;
  description?: string;
  salary?: string;
  deadline?: string;
  status?: "Open" | "Closed" | string;
}

export interface InternshipStats {
  total: number;
  open: number;
  closed: number;
  remote: number;
}
