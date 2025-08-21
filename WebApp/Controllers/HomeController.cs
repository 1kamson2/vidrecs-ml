namespace WebApp.Controllers;

using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using WebApp.Models.Requests;
using WebApp.Models.Responses;
using WebApp.Models.Api;

public class HomeController : Controller
{
    private readonly ILogger<HomeController> _logger;
    private readonly ServiceManager _serviceManager;
    private readonly string _welcomeMessage = "Hello Dear Viewer! Please read About to learn more about this site!";
    private readonly string _errorMessage = "Something went wrong.";

    public HomeController(ILogger<HomeController> logger, ServiceManager serviceManager)
    {
        _logger = logger;
        _logger.LogInformation("Home.");
        _serviceManager = serviceManager;
    }

    [HttpGet]
    public IActionResult Index()
    {
        var respBody = new Response("Tester", "BeingTested", _welcomeMessage);
        return Json(respBody);
    }

    [HttpPost]
    public async Task<IActionResult> Register([FromBody] JsonElement userRequest)
    {
        RegisterRequest registerRequest = RegisterRequest.FromJson(userRequest);
        var registerResult = await _serviceManager.RegisterAttempt(registerRequest);
        return Json(registerResult);
    }

    [HttpPost]
    public async Task<IActionResult> Login([FromBody] JsonElement userRequest)
    {
        LoginRequest loginRequest = LoginRequest.FromJson(userRequest);
        var loginResult = await _serviceManager.LoginAttempt(loginRequest);
        return Json(loginResult);
    }

    [HttpPost]
    public async Task<IActionResult> GameInfo([FromBody] JsonElement userRequest)
    {
        GameRequest gameRequest = GameRequest.FromJson(userRequest);
        var gameRequestResult = await _serviceManager.GameInfoFetchAttempt(gameRequest);
        return Content(gameRequestResult, "application/json");

    }
}
