using Microsoft.AspNetCore.Mvc;
using System.IO;
using System.Net;
using System.Threading.Tasks;
using YoutubeDLSharp;

namespace YoutubeDLServer.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class DownloadController : ControllerBase
    {
        [HttpPost]
        public async Task<IActionResult> Download([FromBody] DownloadRequest request)
        {
            string url = request.Url;
            string downloadPath = request.Path;

            string videoFilePath = Path.Combine(downloadPath, "%(title)s.%(ext)s");

            var youtubeDL = new YoutubeDL();
            youtubeDL.Options.FilesystemOptions.Output = videoFilePath;

            youtubeDL.Options.VideoFormatOptions.Format = "best";

            youtubeDL.Options.DownloadOptions.Progress += (s, e) =>
            {
                if (e.Status == DownloadStatus.Downloading)
                {
                    System.Console.WriteLine($"Downloading... {e.Progress}%");
                }
            };

            await youtubeDL.DownloadAsync(url);

            return Ok(new { status = "success" });
        }
    }

    public class DownloadRequest
    {
        public string Url { get; set; }
        public string Path { get; set; }
    }
}
