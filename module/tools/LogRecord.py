# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='.\\logs\\output.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s',)

logger = logging.getLogger(__name__)