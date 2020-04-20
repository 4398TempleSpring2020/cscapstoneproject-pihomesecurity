using System;
using System.Collections.Generic;

namespace PiHomeSecurityWeb.Models
{
    public partial class Employee
    {
        public int EmployeeId { get; set; }
        public string EmployeeName { get; set; }
        public string EmployeeUsername { get; set; }
        public string EmployeePassword { get; set; }
        public DateTime? LastLogin { get; set; }
    }
}
