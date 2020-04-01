using System;
using System.Collections.Generic;

namespace PiHomeSecurityWeb.Models
{
    public partial class HomeAccount
    {
        public HomeAccount()
        {
            IncidentData = new HashSet<IncidentData>();
            UserAccounts = new HashSet<UserAccounts>();
        }

        public int AccountId { get; set; }
        public string AccountUsername { get; set; }
        public string AccountPassword { get; set; }
        public int AccountPin { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string EmailAddress { get; set; }
        public string HomeAccountAddress { get; set; }
        public long PhoneNumber { get; set; }
        public int? NumOfUsers { get; set; }
        public sbyte AccountActiveFlag { get; set; }
        public long IncidentPhoneNumber { get; set; }

        public virtual ICollection<IncidentData> IncidentData { get; set; }
        public virtual ICollection<UserAccounts> UserAccounts { get; set; }
    }
}
