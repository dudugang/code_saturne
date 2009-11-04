# -*- coding: iso-8859-1 -*-
#
#-------------------------------------------------------------------------------
#
#     This file is part of the Code_Saturne User Interface, element of the
#     Code_Saturne CFD tool.
#
#     Copyright (C) 1998-2007 EDF S.A., France
#
#     contact: saturne-support@edf.fr
#
#     The Code_Saturne User Interface is free software; you can redistribute it
#     and/or modify it under the terms of the GNU General Public License
#     as published by the Free Software Foundation; either version 2 of
#     the License, or (at your option) any later version.
#
#     The Code_Saturne User Interface is distributed in the hope that it will be
#     useful, but WITHOUT ANY WARRANTY; without even the implied warranty
#     of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with the Code_Saturne Kernel; if not, write to the
#     Free Software Foundation, Inc.,
#     51 Franklin St, Fifth Floor,
#     Boston, MA  02110-1301  USA
#
#-------------------------------------------------------------------------------

"""
This module contains the following classes and function:
- Zone
- BoundaryZone
- VolumicZone
- LocalizationModel
- VolumicLocalizationModel
- BoundaryLocalizationModel
- LocalizationVolumicTestCase
- LocalizationSurfacicTestCase
"""

#-------------------------------------------------------------------------------
# Library modules import
#-------------------------------------------------------------------------------

import sys, unittest, types

#-------------------------------------------------------------------------------
# Application modules import
#-------------------------------------------------------------------------------

from Base.XMLvariables import Model
from Base.XMLmodel import ModelTest
from Base.XMLengine import *
from Pages.Boundary import Boundary

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------

class Zone(object):
    """
    Zone API
    """
    def __new__(cls, typeZone , label = None, codeNumber = None, localization = None, nature = None):
        """
        Factory
        """
        if typeZone == 'BoundaryZone':
            return BoundaryZone.__new__(BoundaryZone, label, codeNumber, localization, nature)
        elif typeZone == 'VolumicZone':
            return VolumicZone.__new__(VolumicZone, label, codeNumber, localization)
        else:
            raise ValueError, "Unknown type zone"


    def __init__(self, typeZone , label = None, codeNumber = None, localization = None, nature = None):
        """
        """           
        self._initNatureList()

        if label:
            self._label = label
        else:
            self._label = self.defaultValues()['label']
        if codeNumber:
            self._codeNumber = codeNumber
        else:
            self._codeNumber = self.defaultValues()['codeNumber']
        if localization:
            self._localization = localization
        else:
            self._localization = self.defaultValues()['localization']
        if nature:
            if typeZone == 'VolumicZone' and type(nature) == types.StringType:
                self._nature = self.defaultValues()['nature'].copy()
                self._nature[nature] = "on"
            else:
                self._nature = nature
        else:
            self._nature = self.defaultValues()['nature']


    def _initNatureList(self):
        self._natureList = []
        self._natureDict = {}


    def setLabel(self, text):
        if Model().isStr(text):
            self._label = text


    def getLabel(self):
        return self._label


    def setLocalization(self, text):
        if Model().isStr(text):
            self._localization = text


    def getLocalization(self):
        return self._localization


    def setCodeNumber(self, number):
        if Model().isPositiveInt(number):
            self._codeNumber = number


    def getCodeNumber(self):
        return self._codeNumber


    def setNature(self, text):
        if Model().isInList(text, self._natureList):
            self._nature = text


    def getNature(self):
        return self._nature


    def getNatureList(self):
        return self._natureList


    def getModel2ViewDictionary(self):
        return self._natureDict


    def defaultValues(self):
        dico = {}
        dico['codeNumber'] = -1
        dico['localization'] = "all[]"
        return dico

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------

class BoundaryZone(Zone):
    """
    """
    def __new__(cls, label = None, codeNumber = None, localization = None, nature = None):
        """
        Constructor
        """
        return object.__new__(cls)


    def _initNatureList(self):
        self._natureList = ['wall', 'inlet', 'outlet', 'symmetry']

        self._natureDict = {}
        self._natureDict['wall']     = self.tr("Wall")
        self._natureDict['inlet']    = self.tr("Inlet")
        self._natureDict['outlet']   = self.tr("Outlet")
        self._natureDict['symmetry'] = self.tr("Symmetry")


    def defaultValues(self):
        """
        """
        dico = Zone.defaultValues(self)
        dico['label'] = 'Wall_'
        dico['nature'] = self._natureList[0]
        return dico


    def tr(self, text):
        """
        Translation
        """
        return text

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------

class VolumicZone(Zone):
    """
    """
    def __new__(cls, label = None, codeNumber = None, localization = None, nature = None):
        return object.__new__(cls)


    def _initNatureList(self):
        self._natureList= ['initialization',
                           'head_losses',
                           'momentum_source_term',
                           'mass_source_term',
                           'thermal_source_term',
                           'scalar_source_term']

        self._natureDict = {}
        self._natureDict['initialization']       = self.tr("Initialization")
        self._natureDict['head_losses']          = self.tr("Head losses")
        self._natureDict['momentum_source_term'] = self.tr("Momentum source term")
        self._natureDict['mass_source_term']     = self.tr("Mass source term")
        self._natureDict['thermal_source_term']  = self.tr("Thermal source term")
        self._natureDict['scalar_source_term']   = self.tr("Scalar source term")


    def defaultValues(self):
        dico = Zone.defaultValues(self)
        dico['label'] = 'Zone_'
        dico['nature'] = {}
        dico['nature']['initialization']       = "on"
        dico['nature']['head_losses']          = "off"
        dico['nature']['momentum_source_term'] = "off"
        dico['nature']['mass_source_term']     = "off"
        dico['nature']['thermal_source_term']  = "off"
        dico['nature']['scalar_source_term']   = "off"
        return dico


    def tr(self, text):
        """
        Translation
        """
        return text

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------

class LocalizationModel(object):
    """
    Abstract class
    """
    def __new__(cls, typeZone, case):
        """
        """
        if typeZone == 'BoundaryZone':
            return BoundaryZone.__new__(BoundaryLocalizationModel, case)
        elif typeZone == 'VolumicZone':
            return VolumicZone.__new__(VolumicLocalizationModel, case)
        else:
            raise ValueError, "Unknown type zone"


    def __init__(self, typeZone, case):
        """
        """
        self._case = case
        self._initModel()
        self._typeZone = typeZone


    def getLocalizationsZonesList(self):
        """
        Return list of localizations used by zones
        """
        zones = self.getZones()
        locals = []
        for zone in zones:
            locals.append(zone.getLocalization())
        
        return locals


    def getLabelsZonesList(self):
        """
        Return list of labels used by zones
        """
        zones = self.getZones()
        labels = []
        for zone in zones:
            labels.append(zone.getLabel())

        return labels


    def getCodeNumbersList(self):
        """
        Return list of code numbers used
        """
        zones = self.getZones()
        codes = []
        for zone in zones:
            codes.append(zone.getCodeNumber())
        
        return codes


    def getZones(self):
        """
        Return zones list after XML file reading (virtual method)
        """
        return []


    def getMaxCodeNumber(self):
        """
        Return maximum of code number's values to put on name
        """
        zones = self.getZones()
        codeNumber = 0
        for zone in zones:
            codeNumber = max(codeNumber, zone.getCodeNumber())

        return codeNumber


    def getMaxNumberNature(self, nature):
        """
        Return maximum of nature number's values to put on name
        """
        Model().isInList(nature, self._natureList)


    def renameLabel(self, label, newLabel):
        """
        """
        if label == newLabel: return

        labels = self.getLabelsZonesList()

        Model().isInList(label, labels)
        Model().isNotInList(newLabel, labels)


    def renameName(self, codeNumber, newCodeNumber):
        """
        """
        if codeNumber == newCodeNumber: return

        labels = self.getLabelsZonesList()

        Model().isInt(newCodeNumber)


    def replaceLocalization(self, local, newLocal):
        """
        """
        if local == newLocal: return

        Model().isNotInList(newLocal, self.getLocalizationsZonesList())


    def setLocalization(self, label, localization):
        """
        Define a new localization for the current zone (zone.getLabel == label).
        """
        labels = self.getLabelsZonesList()
        Model().isInList(label, labels)


    def setNature(self, label, nature):
        """
        Define a new nature number for the current zone (zone.getLabel == label) 
        """
        # Set nature: nothing here, see other setNature reimplementation methods
        pass


    def addZone(self, newZone = None):
        """
        Add a new zone. Management of default values.
        """
        if newZone == None:
            newZone = Zone(self._typeZone)

        zones = self.getZones()

        # Set localization

        if newZone.getLocalization() == newZone.defaultValues()['localization']:
            oldLocalization = ""
            newLocalization = ""
            for zone in zones:
                oldLocalization = zone.getLocalization()
                if oldLocalization != "all[]":
                    if newLocalization == "":
                        newLocalization = oldLocalization
                    else:
                        newLocalization += " or " + oldLocalization

            if newLocalization == "":
                newLocalization = newZone.defaultValues()['localization']
            if newLocalization != "all[]":
                newLocalization = "not (" + newLocalization + ")"

            newZone.setLocalization(newLocalization)
        else:
            # No control on localization is avaliable
            pass

        # Set code number

        if newZone.getCodeNumber() == newZone.defaultValues()['codeNumber']:
            newZone.setCodeNumber(self.getMaxCodeNumber() + 1)
        else:
            codes = []
            for zone in zones:
                codes.append(zone.getCodeNumber())
            Model().isNotInList(newZone.getCodeNumber(), codes)

        # Set label: search a free label (Type of newLabel is: "default_n")

        newLabel = newZone.getLabel()
        if newLabel == newZone.defaultValues()['label']:
            code = 1
            inLabels = 1
            while (inLabels):
                inLabels = 0
                for zone in zones:
                    if newLabel+str(code) == zone.getLabel():
                        inLabels = 1
                        break
                code += 1
            newLabel = newLabel + str(code-1)

            newZone.setLabel(newLabel)
        else:
            labels = []
            for zone in zones:
                labels.append(zone.getLabel())
            Model().isNotInList(newLabel, labels)

        # Set nature: nothing here, see other addZone reimplementation methods

        return newZone


    def replaceZone(self, old_zone, new_zone):
        """
        Replace a zone by another in the XML file
        """
        newLabel = new_zone.getLabel()
        if newLabel == new_zone.defaultValues()['label']:
            newLabel = old_zone.getLabel()
        self.renameLabel(old_zone.getLabel(), newLabel)

        newCodeNumber = new_zone.getCodeNumber()
        if newCodeNumber == new_zone.defaultValues()['codeNumber']:
            newCodeNumber = old_zone.getCodeNumber()
        self.renameName(old_zone.getCodeNumber(), newCodeNumber)

        newLocal = new_zone.getLocalization()
        if newLocal == new_zone.defaultValues()['localization']:
            newLocal = old_zone.getLocalization()
        self.replaceLocalization(old_zone.getLocalization(), newLocal)

        return newLabel, newCodeNumber, newLocal


    def deleteZone(self, label):
        """
        Delete the current zone (zone.getLabel == label)
        """
        pass

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------

class VolumicLocalizationModel(LocalizationModel):
    """
    """
    def __new__(cls, case):
        """
        Constructor
        """
        return object.__new__(cls)


    def _initModel(self):
        """
        Initialize mode
        """
        XMLSolutionDomainNode = self._case.xmlInitNode('solution_domain')
        self.__XMLVolumicConditionsNode = XMLSolutionDomainNode.xmlInitNode('volumic_conditions')
        self.__natureOptions = Zone('VolumicZone').getNatureList()
        self._tagList = ['initial_value']


    def getZones(self):
        """
        Get zones in the XML file
        """
        XMLZonesNodes = self.__XMLVolumicConditionsNode.xmlGetChildNodeList('zone', 'label', 'name')

        # XML file reading
        zones = []
        for node in XMLZonesNodes:
            label = str(node['label'])
            codeNumber = int(node['name'])
            localization = str(node.xmlGetTextNode())
            nature = self.getNature(label)
            zone = Zone('VolumicZone',
                        label = label,
                        codeNumber = codeNumber,
                        localization = localization,
                        nature = nature)
            zones.append(zone)
        return zones


    def getCodeNumberOfZoneLabel(self, label):
        """
        Get zones in the XML file
        """
        XMLZonesNodes = self.__XMLVolumicConditionsNode.xmlGetChildNodeList('zone', 'label', 'name')

        # XML file reading
        for node in XMLZonesNodes:
            if node['label'] == label:
                codeNumber = node['name']
        
        return codeNumber


    def setLocalization(self, label, localization):
        """
        Define a new localization for the current zone (zone.getLabel == label)
        Update XML file 
        """
        node = self.__XMLVolumicConditionsNode.xmlGetChildNode('zone', 'name', label = label)
        node.xmlSetTextNode(localization)


    def getCodeNumbersList(self, codeNumber=None):
        """
        Define a new code number for the current zone (zone.getLabel == label)
        Update XML file 
        """
        XMLZonesNodesList = self._case.xmlGetNodeList('zone', 'label', 'name')
        codeList = []
        for node in XMLZonesNodesList:
            codeList.append(node['name'])
        return codeList


    def getNature(self, label):
        """
        Define a new Nature for the current zone (zone.getLabel == label)
        Update XML file 
        """
        node = self.__XMLVolumicConditionsNode.xmlGetChildNode('zone', 'name', label = label)
        nature = {}
        for option in self.__natureOptions:
            if node[option] == 'on':
                nature[option] = 'on'
            else:
                nature[option] = 'off'
        return nature


    def setNature(self, label, nature):
        """
        Define a new Nature for the current zone (zone.getLabel == label)
        Update XML file 
        """
        node = self.__XMLVolumicConditionsNode.xmlGetChildNode('zone', 'name', label = label)
        oldNature = self.getNature(label)
        if oldNature != nature:
            for option in self.__natureOptions:
                if option not in nature.keys():
                    nature[option] = 'off'
            for k,v in nature.items():
                node[k] = v


    def addZone(self, zone = None):
        """
        Add a new zone in the XML file
        """
        newZone = LocalizationModel.addZone(self, zone)

        # XML file updating
        node = self.__XMLVolumicConditionsNode.xmlInitNode('zone',
                                                           label = newZone.getLabel(),
                                                           name = newZone.getCodeNumber())

        for k, v in newZone.getNature().items():
            node[k] = v

        node.xmlSetTextNode(newZone.getLocalization())

        return newZone


    def replaceZone(self, old_zone, new_zone):
        """
        Replace a zone by another in the XML file
        """
        newLabel, newCodeNumber, newLocal = LocalizationModel.replaceZone(self, old_zone, new_zone)

        node = self.__XMLVolumicConditionsNode.xmlGetNode('zone',
                                                           label = old_zone.getLabel())

        # if codeNumber is modified, we must modify zone in initialization of variables
        if old_zone.getCodeNumber() != newCodeNumber:
            node['name'] = newCodeNumber

        node['label'] = newLabel
        node.xmlSetTextNode(newLocal)
        for k, v in new_zone.getNature().items():
            node[k] = v

        # update data in the entire case
        list = self.__natureOptions
        list.append('initial_value')
        list.append('head_loss')
        for tag in list:
            for n in self._case.xmlGetNodeList(tag, zone=old_zone.getCodeNumber()):
                n['zone'] = newCodeNumber
            for n in self._case.xmlGetNodeList(tag, name=old_zone.getCodeNumber()):
                n['name'] = newCodeNumber
            for n in self._case.xmlGetNodeList(tag, label=old_zone.getLabel()):
                n['label'] = newLabel


    def deleteZone(self, label):
        """
        Delete one zone in the XML file
        """
        LocalizationModel.deleteZone(self, label)
        #
        # Delete node
        node = self._case.xmlGetNode('zone', label=label)
        if node:
            name = node['name']
            node.xmlRemoveNode()
            
        # Delete the other nodes for zone initializations
        for tag in self._tagList:
            nodeList = self._case.xmlGetNodeList(tag, zone=name)
            for node in nodeList:
                node.xmlRemoveNode()

#-------------------------------------------------------------------------------
# 
#-------------------------------------------------------------------------------

class BoundaryLocalizationModel(LocalizationModel):
    """
    """
    def __new__(cls, case):
        """
        Constructor
        """
        return object.__new__(cls)


    def _initModel(self):
        """
        Initialize mode
        """
        #LocalizationModel._initModel(self)
        self.__XMLBoundaryConditionsNode = self._case.xmlInitNode('boundary_conditions')
        self.__natureList = Zone('BoundaryZone').getNatureList()


    def getZones(self):
        """
        Get zones in the XML file
        """
        XMLZonesNodes = self.__XMLBoundaryConditionsNode.xmlGetChildNodeList('boundary', 'label', 'name', 'nature')
        #
        # XML file reading
        zones = []
        for node in XMLZonesNodes:
            label = str(node['label'])
            nature = str(node['nature'])
            codeNumber = int(node['name'])
            localization = str(node.xmlGetTextNode())
            zone = Zone('BoundaryZone', label = label, codeNumber = codeNumber, localization = localization, nature = nature) 
            zones.append(zone)
        return zones


    def getMaxNumberNature(self, nature):
        """
        Return maximum of nature number's values to put on name
        """
        
        XMLZonesNodes = self.__XMLBoundaryConditionsNode.xmlGetChildNodeList('boundary', 'label', 'name', 'nature')
        max = 0
        #
        # XML file reading
        zones = []
        for node in XMLZonesNodes:
            if node['nature'] == nature:
                max = max + 1
        return max



    def setLabel(self, label, newLabel):
        """
        Define a new label for the current zone (zone.getLabel == label)
        Update XML file 
        """
        LocalizationModel.renameLabel(self, label, newLabel)
        #
        # XML file updating
        node = self.__XMLBoundaryConditionsNode.xmlGetChildNode('boundary', 'name', 'nature', label = label )
        node['label'] = newLabel
        nature = node['nature']
        #
        # Update references
        XMLZonesNodes = self.__XMLBoundaryConditionsNode.xmlGetChildNodeList(nature, label = label)
        for node in XMLZonesNodes:
            node['label'] = newLabel


    def setLocalization(self, label, localization):
        """
        Define a new localization for the current zone (zone.getLabel == label)
        Update XML file 
        """
        LocalizationModel.setLocalization(self, label, localization)
        #
        # XML file updating
        node = self.__XMLBoundaryConditionsNode.xmlGetChildNode('boundary', 'name', 'nature', label = label)
        node.xmlSetTextNode(localization)


    def setCodeNumber(self, label, codeNumber):
        """
        Define a new code number for the current zone (zone.getLabel == label)
        Update XML file 
        """
        LocalizationModel.setCodeNumber(self, label, codeNumber)
        #
        # XML file updating
        node = self.__XMLBoundaryConditionsNode.xmlGetChildNode('boundary', 'name', 'nature', label = label)
        node['name'] = str(codeNumber)


    def setNature(self, label, nature):
        """
        Define a new Nature for the current zone (zone.getLabel == label)
        Update XML file 
        """
        LocalizationModel.setNature(self, label, nature)

        # XML file updating
        node = self.__XMLBoundaryConditionsNode.xmlGetChildNode('boundary', 'name', 'nature', label = label)
        oldNature = node['nature']
        node['nature'] = str(nature)

        # Delete oldNature boundary 
        Boundary(oldNature, label, self._case).delete()

        # Create nature boundary
        Boundary(nature, label, self._case)


    def addZone(self, zone = None):
        """
        Add a new zone in the XML file
        """
        newZone = LocalizationModel.addZone(self, zone)

        # XML file updating
        node = self.__XMLBoundaryConditionsNode.xmlInitNode('boundary', 
                                                            label = newZone.getLabel(), 
                                                            name = str(newZone.getCodeNumber()),
                                                            nature = newZone.getNature())
        node.xmlSetTextNode(newZone.getLocalization())

        # Create nature boundary
        Boundary(newZone.getNature(), newZone.getLabel(), self._case)

        return newZone


    def replaceZone(self, old_zone, new_zone):
        """
        Replace a zone by another in the XML file
        """
        Boundary(old_zone.getNature(), old_zone.getLabel(), self._case).delete()
        newLabel, newCodeNumber, newLocal = LocalizationModel.replaceZone(self, old_zone, new_zone)

        newNature = new_zone.getNature()
        Model().isInList(newNature, self.__natureList)
        
        node = self.__XMLBoundaryConditionsNode.xmlGetNode('boundary', 
                                                            label = old_zone.getLabel())

        node['label'] = newLabel
        node['name'] = newCodeNumber
        node['nature'] = newNature
        node.xmlSetTextNode(newLocal)

        Boundary(new_zone.getNature(), new_zone.getLabel(), self._case)


    def deleteZone(self, label):
        """
        Delete a zone in the XML file
        """
        LocalizationModel.deleteZone(self, label)

        # Get Nature
        node = self.__XMLBoundaryConditionsNode.xmlGetNode('boundary', 'name', 'nature', label = label)
        nature = node['nature']
        node.xmlRemoveNode()

        # Delete nature boundary 
        Boundary(nature, label, self._case).delete()

#-------------------------------------------------------------------------------
# LocalizationModel test case for volumic zones
#-------------------------------------------------------------------------------

class LocalizationVolumicTestCase(ModelTest):
    """
    Unittest.
    """
    def checkLocalizationInstantiation(self):
        """Check whether the LocalizationModel class could be instantiated."""
        model = None
        model = LocalizationModel("VolumicZone", self.case)
        assert model != None, 'Could not instantiate LocalizationVolumicModel'


    def checkInitialZone(self):
        """Check whether the zone could be initialized"""
        model = LocalizationModel("VolumicZone", self.case)
        node = self.case.xmlGetNode('volumic_conditions')

        doc = '''<volumic_conditions>
                    <zone head_losses="off" initialization="on" label="all_cells" mass_source_term="off" momentum_source_term="off" name="1" thermal_source_term="off">
                            all[]
                    </zone>
                 </volumic_conditions>'''
                 
        assert node == self.xmlNodeFromString(doc),\
           'Could not initialize default volumic zone'


    def checkAddAndDeleteZone(self):
        """Check whether the zone could be added and deleted"""
        model = LocalizationModel("VolumicZone", self.case)
        node = self.case.xmlGetNode('volumic_conditions')
        model.addZone()
        zone = Zone("VolumicZone", label='toto', localization="1 or door")
        model.addZone(zone)
        zone = Zone("VolumicZone", label='fenetre', localization="12 and window or door")
        model.addZone(zone)
        model.addZone()

        doc = '''<volumic_conditions>
                    <zone head_losses="off" initialization="on" label="all_cells" mass_source_term="off" momentum_source_term="off" name="1" thermal_source_term="off">
                            all[]
                    </zone>
                    <zone head_losses="off" initialization="on" label="Zone_1" mass_source_term="off" momentum_source_term="off" name="2" thermal_source_term="off">
                            not(all[])
                    </zone>
                    <zone head_losses="off" initialization="on" label="toto" mass_source_term="off" momentum_source_term="off" name="3" thermal_source_term="off">
                            1 or door
                    </zone>
                    <zone head_losses="off" initialization="on" label="fenetre" mass_source_term="off" momentum_source_term="off" name="4" thermal_source_term="off">
                            12 and window or door
                    </zone>
                    <zone head_losses="off" initialization="on" label="Zone_2" mass_source_term="off" momentum_source_term="off" name="5" thermal_source_term="off">
                            not(all[];not(all[]);1 or door;12 and window or door)
                    </zone>
                </volumic_conditions>'''

        assert node == self.xmlNodeFromString(doc),\
           'Could not add one volumic zone'

        model.deleteZone(label="toto")
        model.deleteZone(label="Zone_2")
        
        doc = '''<volumic_conditions>
                    <zone head_losses="off" initialization="on" label="all_cells" mass_source_term="off" momentum_source_term="off" name="1" thermal_source_term="off">
                            all[]
                    </zone>
                    <zone head_losses="off" initialization="on" label="Zone_1" mass_source_term="off" momentum_source_term="off" name="2" thermal_source_term="off">
                            not(all[])
                    </zone>
                    <zone head_losses="off" initialization="on" label="fenetre" mass_source_term="off" momentum_source_term="off" name="4" thermal_source_term="off">
                            12 and window or door
                    </zone>
                </volumic_conditions>'''

        assert node == self.xmlNodeFromString(doc),\
           'Could not delete one volumic zone'


    def checkReplaceZone(self):
        """Check whether the zone could be replaced"""
        model = LocalizationModel("VolumicZone", self.case)
        node = self.case.xmlGetNode('volumic_conditions')
        model.addZone()
        zone = Zone("VolumicZone", label='toto', localization="1 or door")
        model.addZone(zone)
        zone1 = Zone("VolumicZone", label='fenetre', localization="12 and window or door")
        model.addZone(zone1)
        new_zone = Zone("VolumicZone", label='window', localization="12 or window or door")
##        new_zone = Zone("VolumicZone", localization="12 or window or door")
##        new_zone = Zone("VolumicZone", label='window')

        model.replaceZone(zone1, new_zone)
        
        doc = '''<volumic_conditions>
                    <zone head_losses="off" initialization="on" label="all_cells" mass_source_term="off" momentum_source_term="off" name="1" thermal_source_term="off">
                            all[]
                    </zone>
                    <zone head_losses="off" initialization="on" label="Zone_1" mass_source_term="off" momentum_source_term="off" name="2" thermal_source_term="off">
                            not(all[])
                    </zone>
                    <zone head_losses="off" initialization="on" label="toto" mass_source_term="off" momentum_source_term="off" name="3" thermal_source_term="off">
                            1 or door
                    </zone>
                    <zone head_losses="off" initialization="on" label="window" mass_source_term="off" momentum_source_term="off" name="4" thermal_source_term="off">
                            12 or window or door
                    </zone>
                </volumic_conditions>'''

        assert node == self.xmlNodeFromString(doc),\
           'Could not replace volumic zone'


    def checkSetLabelAndLocalization(self):
        """Check whether the zone could be set label ,and localization"""
        model = LocalizationModel("VolumicZone", self.case)
        node = self.case.xmlGetNode('volumic_conditions')
        model.addZone()
        zone = Zone("VolumicZone", label='toto', localization="1 or door")
        model.addZone(zone)
        zone = Zone("VolumicZone", label='fenetre', localization="12 and window or door")
        model.addZone(zone)

        model.setLocalization("Zone_1", "1 and 2 and 3 or group1")
        doc = '''<volumic_conditions>
                    <zone head_losses="off" initialization="on" label="all_cells" mass_source_term="off" momentum_source_term="off" name="1" thermal_source_term="off">
                            all[]
                    </zone>
                    <zone head_losses="off" initialization="on" label="Zone_1" mass_source_term="off" momentum_source_term="off" name="2" thermal_source_term="off">
                            1 and 2 and 3 or group1
                    </zone>
                    <zone head_losses="off" initialization="on" label="toto" mass_source_term="off" momentum_source_term="off" name="3" thermal_source_term="off">
                            1 or door
                    </zone>
                    <zone head_losses="off" initialization="on" label="fenetre" mass_source_term="off" momentum_source_term="off" name="4" thermal_source_term="off">
                            12 and window or door
                    </zone>
                </volumic_conditions>'''
                
        assert node == self.xmlNodeFromString(doc),\
           'Could not set localization on volumic zone'


    def checkSetAndGetNature(self):
        """Check whether the zone could be set and get nature"""
        model = LocalizationModel("VolumicZone", self.case)
        node = self.case.xmlGetNode('volumic_conditions')
        model.addZone()
        zone = Zone("VolumicZone", label='porte', localization="1 or door")
        model.addZone(zone)
        zone = Zone("VolumicZone", label='fenetre', localization="12 and window or door")
        model.addZone(zone)

        model.setNature('porte', "head_losses,thermal_source_term")

        doc = '''<volumic_conditions>
                    <zone head_losses="off" initialization="on" label="all_cells" mass_source_term="off" momentum_source_term="off" name="1" thermal_source_term="off">
                            all[]
                    </zone>
                    <zone head_losses="off" initialization="on" label="Zone_1" mass_source_term="off" momentum_source_term="off" name="2" thermal_source_term="off">
                            not(all[])
                    </zone>
                    <zone head_losses="on" initialization="off" label="porte" mass_source_term="off" momentum_source_term="off" name="3" thermal_source_term="on">
                            1 or door
                    </zone>
                    <zone head_losses="off" initialization="on" label="fenetre" mass_source_term="off" momentum_source_term="off" name="4" thermal_source_term="off">
                            12 and window or door
                    </zone>
                </volumic_conditions>'''
                
        assert node == self.xmlNodeFromString(doc),\
           'Could not set nature on volumic zone'

        assert model.getNature('fenetre') == "initialization",\
           'Could not get nature on volumic zone'
           
        assert model.getNature('porte') == "thermal_source_term,head_losses",\
           'Could not get nature on volumic zone'


def suite1():
    testSuite = unittest.makeSuite(LocalizationVolumicTestCase, "check")
    return testSuite


def runTest1():
    print __file__
    runner = unittest.TextTestRunner()
    runner.run(suite1())

#-------------------------------------------------------------------------------
# LocalizationModel test case for boundaries conditions
#-------------------------------------------------------------------------------

class LocalizationSurfacicTestCase(ModelTest):
    """
    Unittest.
    """
    def checkLocalizationSurfacicInstantiation(self):
        """
        Check whether the LocalizationModel class could be instantiated 
        for boundary conditions.
        """
        model = None
        model = LocalizationModel("BoundaryZone", self.case)
        assert model != None, 'Could not instantiate LocalizationSurfacicModel'


    def checkAddAndDeleteZone(self):
        """Check whether the zone could be added and deleted for boundary conditions."""
        model = LocalizationModel("BoundaryZone", self.case)
        node = self.case.xmlGetNode('boundary_conditions')
        zone1 = Zone("BoundaryZone", label='entre1', localization="porte", nature='inlet')
        zone2 = Zone("BoundaryZone", label='entre2', localization="fenetre", nature='inlet')
        zone3 = Zone("BoundaryZone", label='plafond', localization="not porte", nature='wall')
        model.addZone(zone1)
        model.addZone(zone2)
        model.addZone(zone3)

        doc = '''<boundary_conditions>
                        <boundary label="entre1" name="1" nature="inlet">
                                porte
                        </boundary>
                        <inlet label="entre1">
                            <velocity_pressure choice="norm">
                            <norm>1</norm>
                            </velocity_pressure>
                            <turbulence choice="hydraulic_diameter">
                                <hydraulic_diameter>1</hydraulic_diameter>
                            </turbulence>
                        </inlet>
                        <boundary label="entre2" name="2" nature="inlet">
                                fenetre
                        </boundary>
                        <inlet label="entre2">
                            <velocity_pressure choice="norm">
                                <norm>1</norm>
                            </velocity_pressure>
                            <turbulence choice="hydraulic_diameter">
                                <hydraulic_diameter>1</hydraulic_diameter>
                            </turbulence>
                        </inlet>
                        <boundary label="plafond" name="3" nature="wall">
                                not porte
                        </boundary>
                        <wall label="plafond">
                            <velocity_pressure choice="off"/>
                        </wall>
                  </boundary_conditions>'''
                  
        model.deleteZone("entre2")

        doc = '''<boundary_conditions>
                        <boundary label="entre1" name="1" nature="inlet">
                                porte
                        </boundary>
                        <inlet label="entre1">
                            <velocity_pressure choice="norm">
                            <norm>1</norm>
                            </velocity_pressure>
                            <turbulence choice="hydraulic_diameter">
                                <hydraulic_diameter>1</hydraulic_diameter>
                            </turbulence>
                        </inlet>
                        <boundary label="plafond" name="3" nature="wall">
                                not porte
                        </boundary>
                        <wall label="plafond">
                            <velocity_pressure choice="off"/>
                        </wall>
                  </boundary_conditions>'''

        assert node == self.xmlNodeFromString(doc),\
           'Could not delete zone in localizationModel for boundaries conditions'


    def checkReplaceZone(self):
        """Check whether the zone could be replaced for boundary conditions."""
        model = LocalizationModel("BoundaryZone", self.case)
        node = self.case.xmlGetNode('boundary_conditions')
        zone1 = Zone("BoundaryZone", label='entre1', localization="porte", nature='inlet')
        zone2 = Zone("BoundaryZone", label='entre2', localization="fenetre", nature='inlet')
        zone3 = Zone("BoundaryZone", label='plafond', localization="not porte", nature='wall')
        model.addZone(zone1)
        model.addZone(zone2)
        model.addZone(zone3)
        zone4 = Zone("BoundaryZone", label='hublot', localization="2 et 3", nature='symmetry')
        model.replaceZone(zone2, zone4)
        
        doc = '''<boundary_conditions>
                        <boundary label="entre1" name="1" nature="inlet">
                                porte
                        </boundary>
                        <inlet label="entre1">
                            <velocity_pressure choice="norm">
                            <norm>1</norm>
                            </velocity_pressure>
                            <turbulence choice="hydraulic_diameter">
                                <hydraulic_diameter>1</hydraulic_diameter>
                            </turbulence>
                        </inlet>
                        <boundary label="hublot" name="2" nature="symmetry">
                                2 et 3
                        </boundary>
                        <boundary label="plafond" name="3" nature="wall">
                                not porte
                        </boundary>
                        <wall label="plafond">
                            <velocity_pressure choice="off"/>
                        </wall>
                        <symmetry label="hublot"/>
                  </boundary_conditions>'''
        
        assert node == self.xmlNodeFromString(doc),\
           'Could not replace zone in localizationModel for boundaries conditions'


def suite2():
    testSuite = unittest.makeSuite(LocalizationSurfacicTestCase, "check")
    return testSuite


def runTest2():
    print __file__
    runner = unittest.TextTestRunner()
    runner.run(suite2())

#-------------------------------------------------------------------------------
# End
#-------------------------------------------------------------------------------

