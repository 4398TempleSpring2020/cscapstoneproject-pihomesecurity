using System;
using System.Diagnostics;
using System.Linq;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using PiHomeSecurityWeb.Models;

namespace PiHomeSecurityWeb.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Index(HomeAccount account)
        {
            using(mypidbContext db = new mypidbContext())
            {
                HomeAccount loggedInAccount = db.HomeAccount.Where(x => x.AccountUsername == account.AccountUsername && x.AccountPassword == account.AccountPassword).FirstOrDefault();
                if(loggedInAccount == null)
                {
                    ViewBag.Message = "Incorrect username or password, please try again";
                    return View();
                }
                else
                {
                    //Save user info to session
                    HttpContext.Session.SetInt32("Id", loggedInAccount.AccountId);
                    HttpContext.Session.SetString("Username", loggedInAccount.AccountUsername);

                    return RedirectToAction("UserTable");
                }
            }
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [HttpGet]
        public IActionResult Emplogon()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Emplogon(Employee emp)
        {
            using (mypidbContext db = new mypidbContext())
            {
                Employee loggedInEmployee = db.Employee.Where(x => x.EmployeeId == emp.EmployeeId && 
                                                                x.EmployeeUsername == emp.EmployeeUsername && 
                                                                x.EmployeePassword == emp.EmployeePassword).FirstOrDefault();
                if (loggedInEmployee == null)
                {
                    ViewBag.Message = "Incorrect credentials, please try again";
                    return View();
                }
                else
                {
                    //Save user info to session
                    HttpContext.Session.SetInt32("Id", loggedInEmployee.EmployeeId);
                    HttpContext.Session.SetString("Username", loggedInEmployee.EmployeeUsername);
                    ViewBag.Employee = "1";

                    return RedirectToAction("EmpTable");
                }
            }
        }
        public IActionResult UserTable()
        {
            ViewBag.Id = HttpContext.Session.GetInt32("Id");
            ViewBag.Username = HttpContext.Session.GetString("Username");
            return View();
        }

        public IActionResult EmpTable()
        {
            return View();
        }

        public IActionResult Info()
        {
            return View();
        }
        [HttpGet]
        public IActionResult Logoff()
        {

            return View();
        }

        [HttpPost]
        public IActionResult Logoff(HomeAccount account)
        {
            try
            {
                HttpContext.Session.Clear();
                return RedirectToAction("Index");

            }
            catch
            {
                return View();

            }
        }

        [HttpGet]
        public ActionResult Register()
        {
            return View();
        }

        [HttpPost]
        public ActionResult Register(HomeAccount account)
        {
            Console.WriteLine("User input data, from register");
            Console.WriteLine("Username: " + account.AccountUsername);
            Console.WriteLine("Password: " + account.AccountPassword);
            Console.WriteLine("Email: " + account.EmailAddress);
            Console.WriteLine("First Name: " + account.FirstName);
            Console.WriteLine("Last Name: " + account.LastName);
            Console.WriteLine("Address: " + account.HomeAccountAddress);
            Console.WriteLine("PIN: " + account.AccountPin);
            Console.WriteLine("Phone Number: " + account.PhoneNumber);


            if (account.AccountPin == 0)
            {
                ViewBag.Message = "Unable to register, PIN must be a numerical value";
            }
            else if(account.PhoneNumber == 0 || account.PhoneNumber.ToString().Length != 10)
            {
                ViewBag.Message = "Unable to register, phone number must be valid";
            }
            else if (!isValidEmail(account.EmailAddress))
            {
                ViewBag.Message = "Unable to register, invalid email address";
            }
            else
            {
                try
                {
                    using (mypidbContext db = new mypidbContext())
                    {
                        db.HomeAccount.Add(account);
                        db.SaveChanges();
                    }
                    ViewBag.Message = account.EmailAddress + " successfully registered";
                }
                catch
                {
                    ViewBag.Message = "Unable to register user, please try again.";
                }
            }
            return View();
        }

        public IActionResult Accounts()
        {
            ViewBag.Id = HttpContext.Session.GetInt32("Id");
            return View();
        }

        [HttpGet]
        public IActionResult EditComment(string id)
        {
            ViewBag.IncidentId = id;
            return View();
        }

        [HttpPost]
        public IActionResult EditComment(string id, IncidentData updatedIncident)
        {
            using (mypidbContext db = new mypidbContext())
            {


                IncidentData incident = db.IncidentData.Where(x => x.IncidentId == id).FirstOrDefault();

                if(incident != null)
                {
                    incident.AdminComments = updatedIncident.AdminComments;
                    db.SaveChanges();
                }
            }
            return RedirectToAction("EmpTable");
        }

        public IActionResult DeleteIncident(string id)
        {
            using (mypidbContext db = new mypidbContext())
            {
                IncidentData deleteMe = db.IncidentData.Where(x => x.IncidentId == id).FirstOrDefault();
                db.IncidentData.Remove(deleteMe);
                db.SaveChanges();
                return RedirectToAction("EmpTable");
            }

        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }

        public bool isValidEmail(string email)
        {
            try
            {
                var addr = new System.Net.Mail.MailAddress(email);
                return addr.Address == email;
            }
            catch
            {
                return false;
            }
        }
    }
}
