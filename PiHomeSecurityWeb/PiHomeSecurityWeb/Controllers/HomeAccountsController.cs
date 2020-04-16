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
    public class HomeAccountsController : ControllerBase
    {
        private readonly mypidbContext _context;

        public HomeAccountsController(mypidbContext context)
        {
            _context = context;
        }

        // GET: api/HomeAccounts
        [HttpGet]
        public async Task<ActionResult<IEnumerable<HomeAccount>>> GetHomeAccount()
        {
            return await _context.HomeAccount.ToListAsync();
        }

        // GET: api/HomeAccounts/5
        [HttpGet("{id}")]
        public async Task<ActionResult<HomeAccount>> GetHomeAccount(int id)
        {
            var homeAccount = await _context.HomeAccount.FindAsync(id);

            if (homeAccount == null)
            {
                return NotFound();
            }

            return homeAccount;
        }

        // PUT: api/HomeAccounts/5
        // To protect from overposting attacks, please enable the specific properties you want to bind to, for
        // more details see https://aka.ms/RazorPagesCRUD.
        [HttpPut("{id}")]
        public async Task<IActionResult> PutHomeAccount(int id, HomeAccount homeAccount)
        {
            if (id != homeAccount.AccountId)
            {
                return BadRequest();
            }

            _context.Entry(homeAccount).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!HomeAccountExists(id))
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

        // POST: api/HomeAccounts
        // To protect from overposting attacks, please enable the specific properties you want to bind to, for
        // more details see https://aka.ms/RazorPagesCRUD.
        [HttpPost]
        public async Task<ActionResult<HomeAccount>> PostHomeAccount(HomeAccount homeAccount)
        {
            _context.HomeAccount.Add(homeAccount);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetHomeAccount", new { id = homeAccount.AccountId }, homeAccount);
        }

        // DELETE: api/HomeAccounts/5
        [HttpDelete("{id}")]
        public async Task<ActionResult<HomeAccount>> DeleteHomeAccount(int id)
        {
            var homeAccount = await _context.HomeAccount.FindAsync(id);
            if (homeAccount == null)
            {
                return NotFound();
            }

            _context.HomeAccount.Remove(homeAccount);
            await _context.SaveChangesAsync();

            return homeAccount;
        }

        private bool HomeAccountExists(int id)
        {
            return _context.HomeAccount.Any(e => e.AccountId == id);
        }
    }
}
