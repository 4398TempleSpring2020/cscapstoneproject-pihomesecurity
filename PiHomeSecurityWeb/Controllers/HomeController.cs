﻿using System;
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
                ViewBag.message = "Unable to register user, please try again.";
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

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
