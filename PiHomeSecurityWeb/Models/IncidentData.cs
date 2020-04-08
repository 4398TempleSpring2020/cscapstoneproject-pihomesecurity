using System;
using System.Collections.Generic;

namespace PiHomeSecurityWeb.Models
{
    public partial class IncidentData
    {
        public string IncidentId { get; set; }
        public int AccountId { get; set; }
        public DateTime DateRecorded { get; set; }
        public sbyte? BadIncidentFlag { get; set; }
        public DateTime? LastAccessed { get; set; }
        public string UserAccessed { get; set; }
        public string AdminComments { get; set; }
        public sbyte DeletionBlockFlag { get; set; }
        public sbyte EmergencyContactedFlag { get; set; }
        public string MicrophonePath { get; set; }
        public string ImagePaths { get; set; }
        public sbyte FriendlyMatchFlag { get; set; }
        public string UltrasonicPath { get; set; }

        public virtual HomeAccount Account { get; set; }
    }
}
