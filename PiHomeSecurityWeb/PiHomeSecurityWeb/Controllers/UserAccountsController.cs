using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using PiHomeSecurityWeb.Models;

namespace PiHomeSecurityWeb.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class UserAccountsController : ControllerBase
    {
        private readonly mypidbContext _context;

        public UserAccountsController(mypidbContext context)
        {
            _context = context;
        }

        // GET: api/UserAccounts
        [HttpGet]
        public async Task<ActionResult<IEnumerable<UserAccounts>>> GetUserAccounts()
        {
            return await _context.UserAccounts.ToListAsync();
        }

        // GET: api/UserAccounts/5
        [HttpGet("{id}")]
        public async Task<ActionResult<UserAccounts>> GetUserAccounts(int id)
        {
            var userAccounts = await _context.UserAccounts.FindAsync(id);

            if (userAccounts == null)
            {
                return NotFound();
            }

            return userAccounts;
        }

        // PUT: api/UserAccounts/5
        // To protect from overposting attacks, please enable the specific properties you want to bind to, for
        // more details see https://aka.ms/RazorPagesCRUD.
        [HttpPut("{id}")]
        public async Task<IActionResult> PutUserAccounts(int id, UserAccounts userAccounts)
        {
            if (id != userAccounts.UserId)
            {
                return BadRequest();
            }

            _context.Entry(userAccounts).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!UserAccountsExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/UserAccounts
        // To protect from overposting attacks, please enable the specific properties you want to bind to, for
        // more details see https://aka.ms/RazorPagesCRUD.
        [HttpPost]
        public async Task<ActionResult<UserAccounts>> PostUserAccounts(UserAccounts userAccounts)
        {
            _context.UserAccounts.Add(userAccounts);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetUserAccounts", new { id = userAccounts.UserId }, userAccounts);
        }

        // DELETE: api/UserAccounts/5
        [HttpDelete("{id}")]
        public async Task<ActionResult<UserAccounts>> DeleteUserAccounts(int id)
        {
            var userAccounts = await _context.UserAccounts.FindAsync(id);
            if (userAccounts == null)
            {
                return NotFound();
            }

            _context.UserAccounts.Remove(userAccounts);
            await _context.SaveChangesAsync();

            return userAccounts;
        }

        private bool UserAccountsExists(int id)
        {
            return _context.UserAccounts.Any(e => e.UserId == id);
        }
    }
}
