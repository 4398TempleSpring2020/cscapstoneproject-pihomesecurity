using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

namespace PiHomeSecurityWeb.Models
{
    public partial class mypidbContext : DbContext
    {
        public mypidbContext()
        {
        }

        public mypidbContext(DbContextOptions<mypidbContext> options)
            : base(options)
        {
        }

        public virtual DbSet<Employee> Employee { get; set; }
        public virtual DbSet<EmployeeHomeRelationship> EmployeeHomeRelationship { get; set; }
        public virtual DbSet<HomeAccount> HomeAccount { get; set; }
        public virtual DbSet<IncidentData> IncidentData { get; set; }
        public virtual DbSet<UserAccounts> UserAccounts { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. See http://go.microsoft.com/fwlink/?LinkId=723263 for guidance on storing connection strings.
                optionsBuilder.UseMySql("server=my-pi-database.cxfhfjn3ln5w.us-east-2.rds.amazonaws.com;port=3306;database=mypidb;uid=web_user;pwd=totallysecurepw#2!", x => x.ServerVersion("5.7.22-mysql"));
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Employee>(entity =>
            {
                entity.HasIndex(e => e.EmployeeId)
                    .HasName("idEmployee_UNIQUE")
                    .IsUnique();

                entity.HasIndex(e => e.EmployeeUsername)
                    .HasName("EmployeeUsername")
                    .IsUnique();

                entity.Property(e => e.EmployeeId)
                    .HasColumnName("EmployeeID")
                    .HasColumnType("int(11)");

                entity.Property(e => e.EmployeeName)
                    .IsRequired()
                    .HasColumnType("varchar(255)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.EmployeePassword)
                    .IsRequired()
                    .HasColumnType("varchar(45)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.EmployeeUsername)
                    .IsRequired()
                    .HasColumnType("varchar(65)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.LastLogin)
                    .HasColumnType("datetime")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");
            });

            modelBuilder.Entity<EmployeeHomeRelationship>(entity =>
            {
                entity.HasNoKey();

                entity.HasIndex(e => e.AccountId)
                    .HasName("AccountID_idx");

                entity.HasIndex(e => e.EmployeeId)
                    .HasName("EmployeeID_idx");

                entity.Property(e => e.AccessDate).HasColumnType("datetime");

                entity.Property(e => e.AccountId)
                    .HasColumnName("AccountID")
                    .HasColumnType("int(11)");

                entity.Property(e => e.EmployeeId)
                    .HasColumnName("EmployeeID")
                    .HasColumnType("int(11)");

                entity.HasOne(d => d.Account)
                    .WithMany()
                    .HasForeignKey(d => d.AccountId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("AccountID");

                entity.HasOne(d => d.Employee)
                    .WithMany()
                    .HasForeignKey(d => d.EmployeeId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("EmployeeID");
            });

            modelBuilder.Entity<HomeAccount>(entity =>
            {
                entity.HasKey(e => e.AccountId)
                    .HasName("PRIMARY");

                entity.HasIndex(e => e.AccountId)
                    .HasName("idCustomer_UNIQUE")
                    .IsUnique();

                entity.HasIndex(e => e.AccountUsername)
                    .HasName("AccountUsername_UNIQUE")
                    .IsUnique();

                entity.HasIndex(e => e.HomeAccountAddress)
                    .HasName("HomeAccountAddress_UNIQUE")
                    .IsUnique();

                entity.Property(e => e.AccountId)
                    .HasColumnName("AccountID")
                    .HasColumnType("int(11)");

                entity.Property(e => e.AccountActiveFlag)
                    .HasColumnType("tinyint(4)")
                    .HasDefaultValueSql("'1'");

                entity.Property(e => e.AccountPassword)
                    .IsRequired()
                    .HasColumnType("varchar(45)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.AccountPin).HasColumnType("int(11)");

                entity.Property(e => e.AccountUsername)
                    .IsRequired()
                    .HasColumnType("varchar(45)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.EmailAddress)
                    .IsRequired()
                    .HasColumnType("varchar(255)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.FirstName)
                    .IsRequired()
                    .HasColumnType("varchar(65)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.HomeAccountAddress)
                    .IsRequired()
                    .HasColumnType("varchar(255)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.IncidentPhoneNumber)
                    .HasColumnType("bigint(11)")
                    .HasDefaultValueSql("'911'");

                entity.Property(e => e.LastName)
                    .IsRequired()
                    .HasColumnType("varchar(65)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.NumOfUsers)
                    .HasColumnType("int(11)")
                    .HasDefaultValueSql("'1'");

                entity.Property(e => e.PhoneNumber).HasColumnType("bigint(11)");
            });

            modelBuilder.Entity<IncidentData>(entity =>
            {
                entity.HasKey(e => e.IncidentId)
                    .HasName("PRIMARY");

                entity.HasIndex(e => e.AccountId)
                    .HasName("idCustomer_idx");

                entity.HasIndex(e => e.IncidentId)
                    .HasName("idIncident_UNIQUE")
                    .IsUnique();

                entity.Property(e => e.IncidentId)
                    .HasColumnName("IncidentID")
                    .HasColumnType("varchar(32)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.AccountId)
                    .HasColumnName("AccountID")
                    .HasColumnType("int(11)");

                entity.Property(e => e.AdminComments)
                    .HasColumnType("varchar(255)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.BadIncidentFlag)
                    .HasColumnType("tinyint(4)")
                    .HasDefaultValueSql("'0'");

                entity.Property(e => e.DateRecorded)
                    .HasColumnType("datetime")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");

                entity.Property(e => e.DeletionBlockFlag)
                    .HasColumnType("tinyint(4)")
                    .HasDefaultValueSql("'1'");

                entity.Property(e => e.EmergencyContactedFlag).HasColumnType("tinyint(4)");

                entity.Property(e => e.FriendlyMatchFlag).HasColumnType("tinyint(4)");

                entity.Property(e => e.ImagePaths)
                    .IsRequired()
                    .HasColumnType("varchar(1054)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.LastAccessed)
                    .HasColumnType("datetime")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");

                entity.Property(e => e.MicrophonePath)
                    .IsRequired()
                    .HasColumnType("varchar(255)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.UltrasonicPath)
                    .IsRequired()
                    .HasColumnType("varchar(255)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.UserAccessed)
                    .HasColumnType("varchar(65)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.HasOne(d => d.Account)
                    .WithMany(p => p.IncidentData)
                    .HasForeignKey(d => d.AccountId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("idCustomer");
            });

            modelBuilder.Entity<UserAccounts>(entity =>
            {
                entity.HasKey(e => e.UserId)
                    .HasName("PRIMARY");

                entity.HasIndex(e => e.AccountId)
                    .HasName("idCustomer_idx");

                entity.HasIndex(e => e.UserId)
                    .HasName("idAccountPermission_UNIQUE")
                    .IsUnique();

                entity.HasIndex(e => e.Username)
                    .HasName("Usermame_UNIQUE")
                    .IsUnique();

                entity.Property(e => e.UserId)
                    .HasColumnName("UserID")
                    .HasColumnType("int(11)");

                entity.Property(e => e.AccountId)
                    .HasColumnName("AccountID")
                    .HasColumnType("int(11)");

                entity.Property(e => e.DateCreated)
                    .HasColumnType("datetime")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");

                entity.Property(e => e.LastLogin)
                    .HasColumnType("datetime")
                    .HasDefaultValueSql("CURRENT_TIMESTAMP");

                entity.Property(e => e.MasterUserFlag).HasColumnType("tinyint(4)");

                entity.Property(e => e.PhoneId)
                    .HasColumnType("varchar(255)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.UserPassword)
                    .IsRequired()
                    .HasColumnType("varchar(45)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.Property(e => e.UserPhoneNumber).HasColumnType("bigint(11)");

                entity.Property(e => e.Username)
                    .IsRequired()
                    .HasColumnType("varchar(65)")
                    .HasCharSet("utf8")
                    .HasCollation("utf8_general_ci");

                entity.HasOne(d => d.Account)
                    .WithMany(p => p.UserAccounts)
                    .HasForeignKey(d => d.AccountId)
                    .OnDelete(DeleteBehavior.ClientSetNull)
                    .HasConstraintName("idCustomer2");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}
