import requests
import click

def upload_package(url, token, file, filename):
    lf = "\r\n"
    boundary = "mc_boundary"

    body =  f"--{boundary}{lf}" 
    body += f"Content-Type: application/vnd.android.application.metadata+json{lf}{lf}"
    body += '{"DeviceFamily":"AndroidPlus"}' + lf +lf
    body += f'--{boundary}{lf}'
    body += f'Content-Type: application/vnd.android.application{lf}'
    body += f'Content-Transfer-Encoding: Binary{lf}'
    body += f'Content-Disposition: attachment; filename="{filename}"{lf}{lf}'
    body += file + lf 
    body += f"--{boundary}--"

    headers = {
        'Authorization': f"Bearer {token}",
        'Accept': "application/json",
        'Content-Type': f"multipart/related; boundary={boundary}",
    }

    try:
        response = requests.post(f"{url}/packages", headers=headers, data=body)
    except Exception as e:
        click.echo(e)

    return response.json()
