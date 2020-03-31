using System;
using System.Collections.Generic;

namespace PiHomeSecurityWeb.Models
{
    public partial class EmployeeHomeRelationship
    {
        public int EmployeeId { get; set; }
        public int AccountId { get; set; }
        public DateTime AccessDate { get; set; }

        public virtual HomeAccount Account { get; set; }
        public virtual Employee Employee { get; set; }
    }
}
