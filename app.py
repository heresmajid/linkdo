from flask import Flask, render_template, request, abort, url_for, jsonify, redirect
from pytube import YouTube
import os


app = Flask(__name__)
app.secret_key = b"\xb7\x1b\xf80\xa6\xcb5\xe6\xda\xd4v+\x18[\x01\x03QB\t2"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")


@app.route("/video")
def youtube_video():
    return render_template("youtube_video.html")


@app.route("/audio")
def youtube_audio():
    return render_template("youtube_audio.html")


@app.route("/download_video", methods=["GET", "POST"])
def download_video():
    if (
        request.method == "POST"
        or request.method == "GET"
        and "vid_url" in request.form
    ):
        url = request.form.get("vid_url")
        yt = YouTube(url)
        title = yt.title
        thumbnail = yt.thumbnail_url

        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=get_download_directory_path())

        data = {"title": title, "thumbnail": thumbnail, "quality": stream.resolution}

        return render_template("youtube_video.html", data=data)

    else:
        return redirect(url_for("youtube_video"))


@app.route("/download_audio", methods=["GET", "POST"])
def download_audio():
    if (
        request.method == "POST"
        or request.method == "GET"
        and "vid_url" in request.form
    ):
        url = request.form.get("vid_url")
        yt = YouTube(url)
        title = yt.title
        thumbnail = yt.thumbnail_url

        streams = yt.streams.filter(only_audio=True)
        high_quality_abr = None
        high_abr = 0

        for s in streams:
            abr = int(s.abr.replace("kbps", ""))
            if abr > high_abr:
                high_abr = abr
                high_quality_abr = s

        high_quality_abr.download(output_path=get_download_directory_path())

        data = {"title": title, "thumbnail": thumbnail}
        return render_template("youtube_audio.html", data=data)
    else:
        return redirect(url_for('youtube_audio'))


def get_download_directory_path():
    """Returns the path to the default download directory."""

    if os.name == "nt":
        # Windows
        return os.path.join(os.environ["USERPROFILE"], "Downloads")
    elif os.name == "posix":
        # macOS, Android and Linux
        return os.path.join(os.environ["HOME"], "Downloads")
    else:
        # Other operating systems
        raise NotImplementedError(f"Operating system {os.name} not supported.")


if __name__ == "__main__":
    app.run(debug=True)
