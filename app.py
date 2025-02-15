from flask import Flask, Response, jsonify, request
import requests
import csv
import io

app = Flask(__name__)

TOKEN = "ProcessoSeletivoStract2025"
BASE_URL = "https://sidebar.stract.to/api"

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "Fernanda Dantas",
        "email": "fer.dantas07@gmail.com",
        "linkedin": "https://www.linkedin.com/in/fernanda-santos-dantas/"
    })


def get_platforms():
    url = f"{BASE_URL}/platforms"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return {platform["value"] for platform in response.json().get("platforms", [])}
    return set()

def get_accounts(platform):
    url = f"{BASE_URL}/api/accounts?platform={{platform}}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json().get("accounts", [])

def get_fields(platform):
    url = f"{BASE_URL}/api/fields?platform={{platform}}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(url, headers=headers)
    return [field["value"] for field in response.json().get("fields", [])]

def get_insights(platform, account, fields):
    url = f"{BASE_URL}/api/insights"
    params = {
        "platform": platform,
        "account": account,
        "token": TOKEN,
        "fields": ",".join(fields)
    }
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(url, params=params, headers=headers)
    return response.json().get("data", [])


@app.route("/platforms", methods=["GET"])
def get_platforms_route():
    platforms = get_platforms()
    return jsonify({"platforms": platforms}), 200


@app.route("/report/<platform>", methods=["GET"])
def get_report(platform):
    valid_platforms = get_platforms()

    if platform not in valid_platforms:
        return jsonify({"error": "Plataforma inválida"}), 400

    accounts_url = f"{BASE_URL}/accounts?platform={platform}"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    accounts_response = requests.get(accounts_url, headers=headers)
    
    if accounts_response.status_code != 200:
        return jsonify({"error": "Erro ao buscar contas"}), 500

    accounts = accounts_response.json().get("accounts", [])

    fields_url = f"{BASE_URL}/fields?platform={platform}"
    fields_response = requests.get(fields_url, headers=headers)
    
    if fields_response.status_code != 200:
        return jsonify({"error": "Erro ao buscar campos"}), 500

    fields = [field["value"] for field in fields_response.json().get("fields", [])]


    output = io.StringIO()
    writer = csv.writer(output)

 
    writer.writerow(["Account ID", "Account Name", "Token", "Available Fields"])

 
    for account in accounts:
        writer.writerow([account["id"], account["name"], account["token"], ", ".join(fields)])


    output.seek(0)
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=report_{platform}.csv"}
    )


@app.route("/<platform>/resumo", methods=["GET"])
def get_platform_summary(platform):
    accounts = get_accounts(platform)
    fields = get_fields(platform)
    summary = {}

    for account in accounts:
        insights = get_insights(platform, account["id"], fields)
        if account["name"] not in summary:
            summary[account["name"]] = {field: 0 for field in fields}
        
        for insight in insights:
            for field in fields:
                if isinstance(insight.get(field), (int, float)):
                    summary[account["name"]][field] += insight[field]

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Platform", "Account Name"] + fields)
    
    for account, data in summary.items():
        writer.writerow([platform, account] + [data[field] for field in fields])

    return output.getvalue(), 200, {"Content-Type": "text/csv"}



@app.route("/geral", methods=["GET"])
def get_general_report():
    platforms = get_platforms()
    all_data = []
    fields_set = set() 

    for platform in platforms:
        accounts = get_accounts(platform)
        platform_fields = get_fields(platform)

       
        fields_set.update(platform_fields)

        for account in accounts:
            insights = get_insights(platform, account["id"], list(fields_set))
            for insight in insights:
                all_data.append([platform, account["name"]] + [insight.get(field, '') for field in fields_set])

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Platform", "Account Name"] + list(fields_set))  
    writer.writerows(all_data)

    return output.getvalue(), 200, {"Content-Type": "text/csv"}


@app.route("/geral/resumo", methods=["GET"])
def get_general_summary():
    platforms = get_platforms()
    summary = {}
    all_data = []
    fields_set = set()

    for platform in platforms:
        accounts = get_accounts(platform)
        platform_fields = get_fields(platform)
        fields_set.update(platform_fields)

        if platform not in summary:
            summary[platform] = {field: 0 for field in fields_set}

        for account in accounts:
            insights = get_insights(platform, account["id"], list(fields_set))
            for insight in insights:
                for field in fields_set:
                    if isinstance(insight.get(field), (int, float)):
                        summary[platform][field] += insight[field]
                all_data.append([platform, account["name"]] + [insight.get(field, '') for field in fields_set])

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Platform"] + list(fields_set))
    
    for platform, data in summary.items():
        writer.writerow([platform] + [data[field] for field in fields_set])

    return output.getvalue(), 200, {"Content-Type": "text/csv"}


if __name__ == "__main__":
    app.run(debug=True)
