# Copyright 2016-2018 Euratom
# Copyright 2016-2018 United Kingdom Atomic Energy Authority
# Copyright 2016-2018 Centro de Investigaciones Energéticas, Medioambientales y Tecnológicas
#
# Licensed under the EUPL, Version 1.1 or – as soon they will be approved by the
# European Commission - subsequent versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at:
#
# https://joinup.ec.europa.eu/software/page/eupl5
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the Licence is distributed on an "AS IS" basis, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.
#
# See the Licence for the specific language governing permissions and limitations
# under the Licence.

import os
import json

from cherab.core.atomic.elements import lookup_element, lookup_isotope


"""
Utilities for managing the local rate repository.
"""

DEFAULT_REPOSITORY_PATH = os.path.expanduser('~/.cherab/openadas/repository')


def encode_transition(transition):
    """
    Generate a key string from a transition.

    Both integer and string transition descriptions are handled.
    """

    upper, lower = transition

    upper = str(upper).lower()
    lower = str(lower).lower()

    return '{} -> {}'.format(upper, lower)


def valid_charge(element, charge):
    """
    Returns true if the element can be ionised to the specified charge state level.

    :param charge: Integer charge state.
    :return: True/False.
    """
    return charge <= element.atomic_number



def _assign_cherab_element(name):

    try:
        element_isotope = lookup_isotope(name)
    except ValueError:
        try:
            element_isotope = lookup_element(name)
        except ValueError:
            raise ValueError("Could not find an element or isotope corresponding to the name  " + name)

    return element_isotope


def _get_elements_charge_from_rates_folder(folder):

    file_list = os.listdir(folder)

    rates = {}
    for i in file_list:
        file_path = os.path.join(folder,file_list[1])
        if not os.path.isdir(file_path) and i.endswith(".json"):
            filename = i.replace(".json","")

            element = _assign_cherab_element(filename)

            rates[filename] = {}
            rates[filename]["element"] = element

            with open(file_path, 'r') as f:
                content = json.load(f)
            rates[filename]["charges"] = list(content.keys())

    return rates


def _available_atomic_rates(rate_type, repository_path=None):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH
    folder_path = os.path.join(repository_path, rate_type + '/')
    file_list = _get_elements_charge_from_rates_folder(folder_path)
    return file_list


def _available_radiated_power_rates(rate_type, repository_path):

    repository_path = repository_path or DEFAULT_REPOSITORY_PATH
    folder_path = os.path.join(repository_path, "radiated_power", rate_type)
    file_list = _get_elements_charge_from_rates_folder(folder_path)
    return file_list


def available_recombination_rates(repository_path=None):

    return _available_atomic_rates("recombination", repository_path)


def available_ionisation_rates(repository_path=None):

    return _available_atomic_rates("ionisation", repository_path)


def available_continuum_radiated_power(repository_path=None):

    return _available_radiated_power_rates("continuum",repository_path)


def available_charge_exchange_radiated_power(repository_path=None):

    return _available_radiated_power_rates("cx",repository_path)


def available_line_radiated_power(repository_path=None):

    return _available_radiated_power_rates("line",repository_path)

