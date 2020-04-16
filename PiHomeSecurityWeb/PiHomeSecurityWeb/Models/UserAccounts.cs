using System;
using System.Collections.Generic;

namespace PiHomeSecurityWeb.Models
{
    public partial class UserAccounts
    {
        public int UserId { get; set; }
        public int AccountId { get; set; }
        public string Username { get; set; }
        public string UserPassword { get; set; }
        public long UserPhoneNumber { get; set; }
        public sbyte MasterUserFlag { get; set; }
        public DateTime DateCreated { get; set; }
        public DateTime LastLogin { get; set; }
        public string PhoneId { get; set; }

        public virtual HomeAccount Account { get; set; }
    }
}
