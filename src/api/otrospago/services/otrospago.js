'use strict';

/**
 * otrospago service
 */

const { createCoreService } = require('@strapi/strapi').factories;

module.exports = createCoreService('api::otrospago.otrospago');
