using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace PiHomeSecurityWeb.Models
{
    public partial class HomeAccount
    {
        public HomeAccount()
        {
            IncidentData = new HashSet<IncidentData>();
            UserAccounts = new HashSet<UserAccounts>();
        }

        [Key]
        public int AccountId { get; set; }

        [Required(ErrorMessage="Username is required.")]
        public string AccountUsername { get; set; }

        [Required(ErrorMessage = "Password is required.")]
        [DataType(DataType.Password)]
        public string AccountPassword { get; set; }

        public int AccountPin { get; set; }

        [Required(ErrorMessage = "First name is required.")]
        public string FirstName { get; set; }

        [Required(ErrorMessage = "Last name is required.")]
        public string LastName { get; set; }

        [Required(ErrorMessage = "Email address is required.")]
        public string EmailAddress { get; set; }

        [Required(ErrorMessage = "Home address is required.")]
        public string HomeAccountAddress { get; set; }

        [Required(ErrorMessage = "Phone number is required.")]
        public long PhoneNumber { get; set; }
        public int? NumOfUsers { get; set; }
        public sbyte AccountActiveFlag { get; set; }
        public long IncidentPhoneNumber { get; set; }

        public virtual ICollection<IncidentData> IncidentData { get; set; }
        public virtual ICollection<UserAccounts> UserAccounts { get; set; }
    }
}
