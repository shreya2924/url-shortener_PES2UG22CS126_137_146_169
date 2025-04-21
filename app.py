from flask import Flask, request, redirect, jsonify, render_template_string

import shortuuid

app = Flask(__name__)
url_store = {}

@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>URL Shortener</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
                h1 { color: #333; }
                .container { margin-top: 20px; }
                input { padding: 8px; width: 70%; margin-right: 10px; }
                button { padding: 8px 16px; background-color: #4285f4; color: white; border: none; cursor: pointer; }
                #result { margin-top: 20px; padding: 10px; display: none; }
                .success { background-color: #e6f4ea; border: 1px solid #34a853; }
                .url-display { font-weight: bold; word-break: break-all; }
            </style>
        </head>
        <body>
            <h1>URL Shortener</h1>
            <div class="container">
                <form id="shortenForm">
                    <input name="url" id="urlInput" placeholder="Enter a URL" required />
                    <button type="submit">Shorten</button>
                </form>
                <div id="result" class="success">
                    <p>Your shortened URL:</p>
                    <p class="url-display"><a id="shortUrl" href="#" target="_blank"></a></p>
                </div>
            </div>

            <script>
                document.getElementById('shortenForm').addEventListener('submit', async function(e) {
                    e.preventDefault();
                    
                    const urlInput = document.getElementById('urlInput').value;
                    
                    try {
                        const response = await fetch('/shorten', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ url: urlInput })
                        });
                        
                        const data = await response.json();
                        
                        if (data.short_url) {
                            const resultDiv = document.getElementById('result');
                            const shortUrlLink = document.getElementById('shortUrl');
                            
                            shortUrlLink.href = data.short_url;
                            shortUrlLink.textContent = data.short_url;
                            resultDiv.style.display = 'block';
                        }
                    } catch (error) {
                        console.error('Error:', error);
                    }
                });
            </script>
        </body>
        </html>
    ''')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    if request.content_type == 'application/json':
        data = request.get_json()
        long_url = data.get('url') if data else None
    else:
        long_url = request.form.get("url")
    
    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    short_id = shortuuid.uuid()[:6]
    url_store[short_id] = long_url
    short_url = request.host_url + short_id
    
    if request.content_type == 'application/json':
        return jsonify({"short_url": short_url})
    else:
        # For form submissions without JavaScript
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>URL Shortened</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
                    h1 { color: #333; }
                    .container { margin-top: 20px; }
                    .success { background-color: #e6f4ea; border: 1px solid #34a853; padding: 10px; }
                    .url-display { font-weight: bold; word-break: break-all; }
                    .button { display: inline-block; margin-top: 15px; padding: 8px 16px; background-color: #4285f4; 
                              color: white; text-decoration: none; }
                </style>
            </head>
            <body>
                <h1>URL Shortened Successfully</h1>
                <div class="container">
                    <div class="success">
                        <p>Your shortened URL:</p>
                        <p class="url-display"><a href="{{ short_url }}">{{ short_url }}</a></p>
                    </div>
                    <a href="/" class="button">Shorten Another URL</a>
                </div>
            </body>
            </html>
        ''', short_url=short_url)

@app.route('/<short_id>')
def redirect_to_original(short_id):
    original_url = url_store.get(short_id)
    if original_url:
        return redirect(original_url)
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>URL Not Found</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }
                h1 { color: #d94235; }
                .error { background-color: #fce8e6; border: 1px solid #d94235; padding: 10px; }
                .button { display: inline-block; margin-top: 15px; padding: 8px 16px; background-color: #4285f4; 
                          color: white; text-decoration: none; }
            </style>
        </head>
        <body>
            <h1>URL Not Found</h1>
            <div class="error">
                <p>The shortened URL you're looking for doesn't exist.</p>
            </div>
            <a href="/" class="button">Go to Homepage</a>
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)