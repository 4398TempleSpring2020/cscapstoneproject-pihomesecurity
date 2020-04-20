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
    public class IncidentDatasController : ControllerBase
    {
        private readonly mypidbContext _context;

        public IncidentDatasController(mypidbContext context)
        {
            _context = context;
        }

        // GET: api/IncidentDatas
        [HttpGet]
        public async Task<ActionResult<IEnumerable<IncidentData>>> GetIncidentData()
        {
            return await _context.IncidentData.ToListAsync();
        }

        // GET: api/IncidentDatas/5
        [HttpGet("{id}")]
        public async Task<ActionResult<IncidentData>> GetIncidentData(string id)
        {
            var incidentData = await _context.IncidentData.FindAsync(id);

            if (incidentData == null)
            {
                return NotFound();
            }

            return incidentData;
        }

        // PUT: api/IncidentDatas/5
        // To protect from overposting attacks, please enable the specific properties you want to bind to, for
        // more details see https://aka.ms/RazorPagesCRUD.
        [HttpPut("{id}")]
        public async Task<IActionResult> PutIncidentData(string id, IncidentData incidentData)
        {
            if (id != incidentData.IncidentId)
            {
                return BadRequest();
            }

            _context.Entry(incidentData).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!IncidentDataExists(id))
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

        // POST: api/IncidentDatas
        // To protect from overposting attacks, please enable the specific properties you want to bind to, for
        // more details see https://aka.ms/RazorPagesCRUD.
        [HttpPost]
        public async Task<ActionResult<IncidentData>> PostIncidentData(IncidentData incidentData)
        {
            _context.IncidentData.Add(incidentData);
            await _context.SaveChangesAsync();

            return CreatedAtAction("GetIncidentData", new { id = incidentData.IncidentId }, incidentData);
        }

        // DELETE: api/IncidentDatas/5
        [HttpDelete("{id}")]
        public async Task<ActionResult<IncidentData>> DeleteIncidentData(string id)
        {
            var incidentData = await _context.IncidentData.FindAsync(id);
            if (incidentData == null)
            {
                return NotFound();
            }

            _context.IncidentData.Remove(incidentData);
            await _context.SaveChangesAsync();

            return incidentData;
        }

        private bool IncidentDataExists(string id)
        {
            return _context.IncidentData.Any(e => e.IncidentId == id);
        }
    }
}
