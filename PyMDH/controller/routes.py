import os
import re
from datetime import datetime

from config.logging import pathLogFile
from config.settings_general import pathApp

from sanic.log import logger
from sanic.response import json, file_stream, text
from sanic import Blueprint
from sanic_openapi import swagger_blueprint, doc

from config import settings_general
from service import srv_example


def logReceivedRequest(func):
    def wrapper(*args, **kwargs):
        logger.info('Receiving: ' + str(args))
        return func(*args, **kwargs)
    return wrapper


def setup_routes(app):
    """
    Author: Lukas Fojtik, Created: 22.1.2020
    Setting up controller paths
    :param app: sanic application object
    :return: N/A
    """

    app.blueprint(swagger_blueprint)

    # Default APIs

    @app.route("/")
    @logReceivedRequest
    async def root(request):
        return json({settings_general.APP_NAME : settings_general.APP_VERSION})


    # Management APIs - for purposes of managing application online

    bpMng = Blueprint("App Management", url_prefix="/mng")

    @bpMng.route("/stop", methods=["POST"])
    @doc.description("Stops Sanic server (close main event loop)")
    @logReceivedRequest
    async def stop(request):
        app.stop()
        return json({'state' : 'stopping'})


    @bpMng.route("/log", methods=["GET"])
    @doc.description("Returns text of app.log. With parameter mode=tail returns last 6 KB")
    @doc.consumes(doc.String(name="mode"))
    @logReceivedRequest
    async def log(request):

        mode = request.args.get('mode')
        print(mode)

        if mode == 'tail':
            # with open(pathLogFile) as fh:
            #     tailedLog = fh.read().splitlines()[-20:]

            with open(pathLogFile, 'rb') as file:
                file.seek(-6144, os.SEEK_END)  # Note minus sign
                tailedLog = file.read().decode()

            return text(tailedLog)

        elif mode is None:
            return await file_stream(pathLogFile)
        else:
            return text('Unknown value of mode parameter: ' + mode)


    pathSettings = os.path.join(pathApp, 'config', 'settings.py')

    @bpMng.route("/settings", methods=["GET"])
    @doc.description("Returns content of settings file.")
    @logReceivedRequest
    async def settings(request):

        return await file_stream(pathSettings)

    @bpMng.route("/settings", methods=["PUT"])
    @doc.description("Change content of settings file for one variable. Arguments: property -> name of property, value -> value to be changed. WARNING: changing of setting cause app to restart itself. (Do it between schedules..)")
    @doc.consumes(doc.String(name="property"), doc.String(name="value"))
    @logReceivedRequest
    async def settings(request):

        property = request.args.get('property')
        value = request.args.get('value')

        print(property, value)

        with open(pathSettings, 'r+') as fh:
            textWhole = fh.read()
            textProperty = re.findall(property+'.*', textWhole)
            textPropertyString = ""
            textPropertyString = textPropertyString.join(textProperty)
            textPropertyString2b = property+" = "+value
            textWhole = re.sub(textPropertyString, textPropertyString2b, textWhole)
            fh.seek(0)
            fh.write(textWhole)
            fh.truncate()

        return text('Property: "'+textPropertyString+'" was changed to: "'+textPropertyString2b+'"')


    app.blueprint(bpMng)


    # Checks APIs - processing of request for getting actual monitoring data related to that particular check

    bpChecks = Blueprint("Monitoring Checks", url_prefix="/check")

    @bpChecks.route("/example")
    @doc.description("Example check")
    @logReceivedRequest
    async def example():

        startTaskTime = datetime.now()
        return json(await srv_example.getResults(startTaskTime))

    app.blueprint(bpChecks)

