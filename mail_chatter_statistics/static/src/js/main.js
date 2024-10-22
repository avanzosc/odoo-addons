odoo.define('mail_chatter_statistics.main', function (require) {
    'use strict';

    const rpc = require('web.rpc');
    const core = require('web.core');
    const QWeb = core.qweb;

    // Inicializar el evento al cargar el módulo
    initChatterStatistics();

    function initChatterStatistics() {
        console.log('Inicializando el módulo de estadísticas de Chatter');

        // Obtener el modelo y el ID desde la URL cuando el DOM esté listo
        const { model, id } = getModelAndIdFromUrl();
        if (model && id) {
            console.log('Llamando a la acción para obtener el Chatter Message ID y Mailing Trace IDs automáticamente');
            callChatterAction(model, id);
        } else {
            console.warn("No se ha podido obtener el modelo o el ID para Chatter");
        }
    }

    function callChatterAction(modelName, recordId) {
        console.log('Llamando a la acción personalizada para el modelo:', modelName, 'y registro ID:', recordId);

        // Comenzar la consulta RPC
        console.log('Iniciando consulta RPC para obtener Chatter Message ID y Mailing Trace IDs...');

        rpc.query({
            model: 'mailing.trace',
            method: 'get_chatter_id',
            args: [modelName, recordId],
        }).then(function (result) {
            console.log('Resultado de la consulta RPC:', result);
            
            // Log para verificar si se encontró el Chatter Message ID
            if (result.chatter_message_id) {
                console.log('Chatter Message ID encontrado:', result.chatter_message_id);
            } else {
                console.warn('No se encontró Chatter Message ID');
            }

            const chatterMessageId = result.chatter_message_id || 'No se encontró Chatter Message ID';
            displayChatterMessageId(chatterMessageId);

            const mailingTraceIds = result.mailing_trace_ids || [];
            console.log('Mailing Trace IDs obtenidos:', mailingTraceIds);

            // Log para verificar el contenido de mailingTraceIds
            if (mailingTraceIds.length > 0) {
                console.log('Se encontraron Mailing Trace IDs:', mailingTraceIds);
            } else {
                console.warn('No se encontraron Mailing Trace IDs');
            }

            displayMailingTraceIds(mailingTraceIds);
        }).catch(function (error) {
            console.error('Error al obtener el Chatter Message ID o los Mailing Trace IDs:', error);
        });
    }

    function getModelAndIdFromUrl() {
        console.log('Accediendo al fragmento de la URL');

        const hash = window.location.hash.substring(1); // Eliminar el '#'
        console.log('Fragmento de URL:', hash);

        const params = new URLSearchParams(hash);
        const model = params.get('model');
        const id = params.get('id');

        console.log('Modelo:', model, 'ID:', id);
        return { model, id };
    }
        
    function displayChatterMessageId(chatterMessageId) {
        console.log('Mostrando Chatter Message ID:', chatterMessageId);
        const chatterIdElement = document.querySelector('.your-chatter-id-selector');
        if (chatterIdElement) {
            chatterIdElement.innerText = chatterMessageId;
        } else {
            console.warn('Elemento para mostrar el Chatter Message ID no encontrado');
        }
    }

    function displayMailingTraceIds(mailingTraceIds) {
        console.log('Mostrando Mailing Trace IDs:', mailingTraceIds);
        const mailingTraceIdElement = document.querySelector('.your-mailing-trace-ids-selector');
        if (mailingTraceIdElement) {
            mailingTraceIdElement.innerText = mailingTraceIds.join(', '); // Mostrar IDs separados por coma
        } else {
            console.warn('Elemento para mostrar los Mailing Trace IDs no encontrado');
        }
    }
});
