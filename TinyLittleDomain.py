import flask
import typing
import backend

app = flask.Flask(__name__, static_url_path='')


@app.route("/check_domain")
def check_domain():
    """ API route to check if a domain exists. """

    domain = flask.request.args.get('domain', '')

    if not backend.is_valid_domainname(domain):
        return flask.jsonify(success=False, message='Invalid domain name')

    server = flask.request.args.get('resolver', '')

    try:
        servers = backend.get_resolver_list(server)
    except KeyError:
        return flask.jsonify(success=False, message='Invalid server')

    try:
        existence = backend.does_domain_exist(domain, servers)
        return flask.jsonify(success=True, domain=domain, existence=existence)
    except:
        return flask.jsonify(success=False,
                             message='Unknown error resolving domain')

@app.route('/data/tlds.json')
def send_tlds():
    return flask.jsonify(tlds=backend.TLDS)

@app.route("/")
def send_home():
    return flask.send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def send_static(path):
    return flask.send_from_directory('static', path)


if __name__ == '__main__':
    app.run()
