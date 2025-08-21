using WebApp.Models.Api;
using WebApp.Interfaces;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllersWithViews();
// builder.Services.AddSingleton<ServiceManager>();
builder.Services.AddHttpClient<ServiceManager>(
        "ServiceApi",
        client =>
        {
            // TODO: Hardcoded, make it read it from the file later.
            // WARNING: Change the address.
            client.BaseAddress = new Uri("http://localhost:9999/");
            client.DefaultRequestHeaders.Add("Accept", "application/json");
        }
);

var app = builder.Build();
app.UseHttpsRedirection();
app.UseRouting();
app.UseAuthorization();
app.MapStaticAssets();
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}")
    .WithStaticAssets();

app.Run();


/* TODO: 
 * Normalize {Login, Register}From class.
 */
