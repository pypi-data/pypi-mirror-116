import numpy as np
from pycalphad import Model, variables as v
from pycalphad.codegen.callables import build_callables

setattr(v, 'GE', v.StateVariable('GE'))

def createModels(db, elements, phases, models = None):
    '''
    Creates models and callables for free energy functions
    This can be used to make equilibrium calculations a bit faster if multiple conditions are used

    Parameters
    ----------
    db : Database
    elements : list
        List of elements to consider
    phases : list
        List of phases to consider
    models : dict {str: Model} (optional)
        Dictionary of Model classes to use
    '''
    m = {p: Model(db, elements, p) for p in phases} if models is None else models
    c = build_callables(db, elements, phases, m, build_gradients = True, build_hessians = True)
    return m, c

def _extractEq(model, eq):
    '''
    Returns equilibrium results of single phase determined by model

    Parameters
    ----------
    model : Model
        Model class for specified phase
    eq : Dataset of a pycalphad equilibrium result
    '''
    return eq.where(eq.Phase == model.phase_name, drop = True)

def site_fraction_elements(model):
    '''
    Returns site fraction elements in order of sublattice and element (alphabetically)

    Parameters
    ----------
    model : Model
        Model class of specified phase
    '''
    siteFractionElements = []
    for fs in model.constituents:
        subElements = []
        for c in fs:
            subElements.append(c.name)
        siteFractionElements = np.concatenate((siteFractionElements, np.sort(subElements)))
    return siteFractionElements

def symbols(model):
    '''
    Returns all symbols in a given model

    Parameters
    ----------
    model : Model
    '''
    return model.state_variables + model.site_fractions

def symbol_map(model, eq):
    '''
    Creates map of symbols pertaining to each site fraction, temperature, pressure

    Parameters
    ----------
    model : Model
        Model class for specified phase
    eq : Dataset from pycalphad equilibrium result

    Returns
    -------
    Array of (symbol, value)
    '''
    #Grab phase data from equilibrium results, if phase is not stable, then we can skip this calculation
    eqsub = _extractEq(model, eq)
    if len(eqsub.Phase.values.ravel()) == 0:
        raise Exception('{} is not a stable phase, cannot extract symbols'.format(model.phase_name))

    #Grab state variables and site fraction values
    SV = [(var, eqsub[var.name].values.ravel()[0]) for var in model.state_variables]
    y = eqsub.Y.values.ravel()

    #Create (symbol, value) map for site fractions and state variables
    return SV + [(model.site_fractions[i], y[i]) for i in range(len(model.site_fractions))]

def update_constituent_index(model, subIndex, constituentIndex):
    '''
    Iterates to next pair of sublattice indices and constituent indices

    Parameters
    ----------
    model : Model
        Model class of specified phase
    subIndex : int
        current sublattice index
    consituentIndex : int
        current constituent index

    Returns
    -------
    Updated (subIndex, constituentIndex)
    '''
    constituentIndex += 1
    if constituentIndex >= len(model.constituents[subIndex]):
        subIndex += 1
        constituentIndex = 0
    return subIndex, constituentIndex

def melement(model, eq):
    '''
    Returns total mole of the phase and moles of each element (un-normalized)

    Parameters
    ----------
    model : Model
        Model class for specified phase
    eq : Dataset from pycalphad equilibrium result

    Returns
    -------
    (Me, dMedy, M) where
        Me - dictionary of total moles for [element]
        dMedy - dictionary of arrays of site fraction derivatives for [element, site fraction]
        M - total moles of the phase
    '''
    eqsub = _extractEq(model, eq)
    symbolMap = symbol_map(model, eqsub)
    yEle = site_fraction_elements(model)

    components = eqsub.component.values.ravel()
    Me = {c: 0 for c in components}
    dMedy = {c: np.zeros(len(yEle)) for c in components}

    subIndex = 0
    constituentIndex = 0
    for i in range(len(model.site_fractions)):
        if yEle[i] != 'VA':
            Me[yEle[i]] += model.site_ratios[subIndex] * symbolMap[len(model.state_variables) + i][1]
            dMedy[yEle[i]][i] = model.site_ratios[subIndex]

        subIndex, constituentIndex = update_constituent_index(model, subIndex, constituentIndex)

    M = np.sum([Me[e] for e in Me])

    return Me, dMedy, M

def dx_dy(model, eq):
    '''
    Derivative of composition with respect to site fractions
    This is just dMedy / M using terms from the melement method

    Parameters
    ----------
    model : Model
        Model class for specified phase
    eq : Dataset from pycalphad equilibrium result
    '''
    Me, dMedy, M = melement(model, eq)
    dMedy = np.array([dMedy[A] for A in dMedy]).transpose()
    return dMedy / M

def dG_dP(self, model, eq, param, symbolMap = None):
    '''
    Derivative of free energy with respect to a given parameter(s)

    Parameters
    ----------
    eq : Dataset from pycalphad equilibrium results
    param : Symbol or array of Symbol
        Derivative of Gibbs free energy will be taken with respect to these symbols
    symbolMap : array of (symbol, value) (optional)

    Returns
    -------
    Array of float of derivatives in same order as param
    '''
    eqsub = _extractEq(model, eq)
    if not hasattr(param, '__len__'):
        param = [param]

    symbolMap = self.symbol_map(eqsub) if symbolMap is None else symbolMap
    return float(self.ast.diff(*param).subs(symbolMap))

def dG_dy(model, eq, symbolMap = None, callables = None):
    '''
    First derivative with respect to site fractions

    Parameters
    ----------
    model : Model
        Model class for specified phase
    eq : Dataset from pycalphad equilibrium results
    symbolMap : array of (symbol, value) from eq (optional)
    callables : dict (optional)
        Pre-computed callables functions for each model
    
    Returns
    -------
    Array of floats for each derivative
    Derivatives will be in same order as site fractions are given in symbolMap
    '''
    if callables is None:
        return np.array([dG_dP(model, eq, [sf], symbolMap) for sf in model.site_fractions])
    else:
        symbolMap = symbol_map(model, eq) if symbolMap is None else symbolMap
        values = [v for s, v in symbolMap]
        return np.array(callables['GM']['grad_callables'][model.phase_name](*values))[len(model.state_variables):]

def d2G_dydy(model, eq, symbolMap = None, callables = None):
    '''
    Second derivative with respect to site fractions

    Parameters
    ----------
    model : Model
        Model class for specified phase
    eq : Dataset from pycalphad equilibrium results
    symbolMap : array of (symbol, value) from eq (optional)
    callables : dict (optional)
        Pre-computed callables functions for each model
    
    Returns
    -------
    Matrix of floats for each second derivative
    Derivatives along each axis will be in same order
        as site fractions are given in symbolMap
    '''
    if callables is None:
        return np.array([[dG_dP(model, eq, [s1, s2], symbolMap) for s1 in model.site_fractions] for s2 in model.site_fractions])
    else:
        symbolMap = symbol_map(model, eq) if symbolMap is None else symbolMap
        values = [v for s, v in symbolMap]
        return np.array(callables['GM']['hess_callables'][model.phase_name](*values))[len(model.state_variables):, len(model.state_variables):]


def hessian(chemical_potentials, composition_set):
    '''
    Returns the hessian of the objective function for a single phase

    Parameters
    ----------
    chemical_potentials : 1-D ndarray
    composition_set : pycalphad.core.composition_set.CompositionSet
    
    Returns
    -------
    Matrix of floats for each second derivative
    Derivatives along each axis will be in order of:
        site fractions, phase amount, lagrangian multipliers, chemical potential
    '''
    elements = list(composition_set.phase_record.nonvacant_elements)
    x = np.array(composition_set.X)
    mu = np.asarray(chemical_potentials)
    dxdy = np.zeros((len(elements), len(composition_set.dof)))
    for comp_idx in range(len(elements)):
        composition_set.phase_record.formulamole_grad(dxdy[comp_idx, :], composition_set.dof, comp_idx)
    dg = np.zeros(len(composition_set.dof))
    composition_set.phase_record.formulagrad(dg, composition_set.dof)
    d2g = np.zeros((len(composition_set.dof), len(composition_set.dof)))
    composition_set.phase_record.formulahess(d2g, composition_set.dof)

    phase_dof = composition_set.phase_record.phase_dof
    num_internal_cons = composition_set.phase_record.num_internal_cons
    num_statevars = composition_set.phase_record.num_statevars
    #Create hessian matrix
    hess = np.zeros((phase_dof + num_internal_cons + len(elements) + 1,
                     phase_dof + num_internal_cons + len(elements) + 1))
    # wrt phase dof
    hess[:phase_dof, :phase_dof] = d2g[composition_set.phase_record.num_statevars:,
                                       composition_set.phase_record.num_statevars:]
    cons_jac_tmp = np.zeros((num_internal_cons, len(composition_set.dof)))
    composition_set.phase_record.internal_cons_jac(cons_jac_tmp, composition_set.dof)

    # wrt phase amount
    for i in range(phase_dof):
        hess[i, phase_dof] = dg[num_statevars + i] - np.sum(mu * dxdy[:, num_statevars+i])
        hess[phase_dof, i] = hess[i, phase_dof]

    hess[:phase_dof, phase_dof+1:phase_dof+1+num_internal_cons] = -cons_jac_tmp[:, num_statevars:].T
    hess[phase_dof+1:phase_dof+1+num_internal_cons, :phase_dof] = hess[:phase_dof, phase_dof+1:phase_dof+1+num_internal_cons].T
    index = phase_dof + num_internal_cons + 1
    hess[:phase_dof, index:] = -1 * dxdy[:, num_statevars:].T
    hess[index:, :phase_dof] = -1 * dxdy[:, num_statevars:]

    for A in range(len(elements)):
        hess[phase_dof, index + A] = -x[A]
        hess[index + A, phase_dof] = -x[A]
    return hess


def totalddx(chemical_potentials, composition_set, refElement):
    '''
    Total derivative of site fractions, phase amount, lagrangian multipliers 
    and chemical potential with respect to system composition
    d/dx = partial d/dxA - partial d/dxR where R is reference

    Parameters
    ----------
    chemical_potentials : 1-D ndarray
    composition_set : pycalphad.core.composition_set.CompositionSet
    refElement : str
        Reference element
    
    Returns
    -------
    Array of floats for each derivative
    Derivatives will be in order of:
        site fractions, phase amount, lagrangian multipliers, chemical potential
    '''
    elements = list(composition_set.phase_record.nonvacant_elements)
    b = np.zeros((composition_set.phase_record.phase_dof + composition_set.phase_record.num_internal_cons + len(elements) + 1, len(elements) - 1))
    i0 = composition_set.phase_record.phase_dof + composition_set.phase_record.num_internal_cons + 1

    c = 0
    for A in range(len(elements)):
        if elements[A] != refElement:
            b[i0 + A, c] = -1
            c += 1
        else:
            b[i0 + A, :] = 1

    #If curvature is undefined, then assume inverse is 0
    #For derivatives with respect to composition, this means that the internal DOFs of the phase is independent of composition
    try:
        inverse = np.linalg.inv(hessian(chemical_potentials, composition_set))
        return np.matmul(inverse, b)
    except:
        return np.zeros(b.shape)


def partialddx(chemical_potentials, composition_set):
    '''
    Partial derivative of site fractions, phase amount, lagrangian multipliers 
    and chemical potential with respect to system composition

    Parameters
    ----------
    chemical_potentials : 1-D ndarray
    composition_set : pycalphad.core.composition_set.CompositionSet
    
    Returns
    -------
    Array of floats for each derivative
    Derivatives will be in order of:
        site fractions, phase amount, lagrangian multipliers, chemical potential
    '''
    elements = list(composition_set.phase_record.nonvacant_elements)
    b = np.zeros((composition_set.phase_record.phase_dof + composition_set.phase_record.num_internal_cons + len(elements) + 1, len(elements)))
    i0 = composition_set.phase_record.phase_dof + composition_set.phase_record.num_internal_cons + 1

    for A in range(len(elements)):
        b[i0 + A, A] = -1

    #If curvature is undefined, then assume inverse is 0
    #For derivatives with respect to composition, this means that the internal DOFs of the phase is independent of composition
    try:
        inverse = np.linalg.inv(hessian(chemical_potentials, composition_set))
        return np.matmul(inverse, b)
    except np.linalg.LinAlgError:
        return np.zeros(b.shape)


def dMudX(chemical_potentials, composition_set, refElement):
    '''
    Total derivative of chemical potential with respect to system composition
    dmu/dx = partial dmu/dxA - partial dmu/dxR where R is reference

    Parameters
    ----------
    chemical_potentials : 1-D ndarray
    composition_set : pycalphad.core.composition_set.CompositionSet
    refElement : str
        Reference element
    
    Returns
    -------
    Array of floats for each derivative
    Derivatives will be in alphabetical order of elements
    '''
    ddx = totalddx(chemical_potentials, composition_set, refElement)
    i0 = composition_set.phase_record.phase_dof + composition_set.phase_record.num_internal_cons + 1
    elements = list(composition_set.phase_record.nonvacant_elements)
    
    dmudx = np.zeros((len(elements) - 1, len(elements) - 1))

    c = 0
    for A in range(len(elements)):
        if elements[A] != refElement:
            dmudx[c, :] += ddx[i0 + A, :]
            c += 1
        else:
            for B in range(len(elements) - 1):
                dmudx[B, :] -= ddx[i0 + A, :]

    return dmudx

def partialdMudX(chemical_potentials, composition_set):
    '''
    Partial derivative of chemical potential with respect to system composition

    Parameters
    ----------
    composition_set : pycalphad.core.composition_set.CompositionSet
    
    Returns
    -------
    Array of floats for each derivative
    Derivatives will be in alphabetical order of elements
    '''
    ddx = partialddx(chemical_potentials, composition_set)
    i0 = composition_set.phase_record.phase_dof + composition_set.phase_record.num_internal_cons + 1
    
    return ddx[i0:,:]
