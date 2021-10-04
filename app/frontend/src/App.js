import React from 'react'
import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import axios from 'axios'
import { loadServerData, initServer } from './services/server'

import store, {addRef, updateRef, makeId, parseId, addSname, updateSname, addName, updateName, addRel, updateRel, mapId, initMapvalues} from './store.js'

const Dropdown = ({name, options, value, onChange}) => {
	return(
		<select name= {name} onChange={onChange} value={value}>
			<option></option>
			{ options.map(tuple => <option key={tuple[0]} value={tuple[0]}>{tuple[1]}</option> )}
		</select>
	)
}

const NameEntry = ({id, data}) => {
	const dispatch = useDispatch()
	const name = data.names.find(v => v.id === id)

	const update = ({target}, field) => {
		const temp = {...name}
		temp[field] = target.value
		dispatch(updateName(data.id, temp, id))
	}

	const updatevariant = newVariant => {
		const value = parseId(id).value
		const temp = {...name, id: makeId(newVariant, value), variant: newVariant}
		dispatch(updateName(data.id, temp, id))
	}

	const qualifierOptions = [
		[`bio`, `Biostratigraphy`],
		[`chemo`, `Chemostratigraphy`],
		[`chrono`, `Chronostratigraphy`],
		[`litho`,`Lithostratigraphy`],
		[`region`, `Regional Standard`],
		[`seq`, `Sequence-stratigraphy`]
	]

	const levelOptions = [
		[1, `1`],
		[2, `2`],
		[3, `3`],
		[4, `4`],
		[5, `5`],
		[6, `6`],
		[7, `7`]
	]

	const variantOptions = [
		[`name`, `Name`],
		[`location`, `Location`],
		[`qualifier`, `Qualifier`]
	]

	return (
		<div>
			<input type="text" name="name" value={name.name} onChange={e => update(e, `name`)} />
			<label htmlFor="variant">Type:</label>
			<Dropdown name="variant" onChange={e => updatevariant(e.target.value)} options={variantOptions} value={name.variant} />
			{ name.variant === `qualifier`
				?<>
				<label htmlFor="qualifier">Qualifier Name:</label>
				<Dropdown name="qualifier" onChange={e => update(e, `qualifier`)} options={qualifierOptions} value={name.qualifier} />
				<label htmlFor="level">Level:</label>
				<Dropdown name="level" onChange={e => update(e, `level`)} options={levelOptions} value={name.level} />
				</>
				: <></> }
		</div>
	)
}

const NameList = ({data}) => {
	const dispatch = useDispatch()
	const addNew = e => {
		const name = {id: makeId(`name`), name: ``, variant: `name`, qualifier: `bio`, level: 1}
		dispatch(addName(data.id, name))
	}

	return (
		<div>
			{data.names.map(v => <NameEntry {...{key: v.id, id: v.id, data}} />)}
			<button type="button" onClick={addNew}>Add new name</button>
		</div>
	)
}

const Ref = ({data}) => {
	const dispatch = useDispatch()

	const doiSubmit = async e => {
		e.preventDefault()
		const doi = e.target.doi.value
		const result = await axios.get(`https://api.crossref.org/works/${doi}`)
		const response = JSON.parse(result.request.response).message

		if (!response.first_author)
			return

		dispatch(updateRef({
			...data,
			queried: true,
			first_author: `${response.first_author[0].given} ${response.first_author[0].family}`,
			year: response.created["date-parts"][0][0],
			title: response.title,
			doi: response.DOI,
			link: response.URL
		}))
	}

	const update = ({target}, field) => {
		const r = {...data}
		r[field] = target.value
		dispatch(updateRef(r))
	}

	if (data.queried)
		return (
			<div>
				<form>
					<label htmlFor="first_author">first_author</label>
					<input type="text" name="first_author" value={data.first_author} onChange={e => update(e, `first_author`)} />
					<br />
					<label htmlFor="year">year</label>
					<input type="text" name="year" value={data.year} onChange={e => update(e, `year`)} />
					<br />
					<label htmlFor="title">title</label>
					<input type="text" name="title" value={data.title} onChange={e => update(e, `title`)} />
					<br />
					<label htmlFor="doi">doi</label>
					<input type="text" name="doi" value={data.doi} onChange={e => update(e, `doi`)} />
					<br />
					<label htmlFor="link">link</label>
					<input type="text" name="link" value={data.link} onChange={e => update(e, `link`)} />
				</form>
				<NameList {...{data}} />
			</div>
		)

	return (
		<div>
			<form onSubmit={doiSubmit}>
				<label htmlFor="doi">doi</label>
				<input type="text" name="doi" name="doi" value={data.doi} onChange={e => update(e, `doi`)} />
				<button type="submit">get</button>
				<button type="button" onClick={() => {dispatch(updateRef({...data, queried: true}))}}>Manual Entry</button>
			</form>
		</div>
	)
}

const findRef = (refs, ids) => refs.find(ref => ref.names.find(v => ids.includes(v.id)))
const findId = (state, id) => state.map[id]

const formatQualifier = (qualifier, state) => {
	if (qualifier === undefined)
		return ``

	const idObject = parseId(qualifier.id)
	if (idObject.type !== `qualifier` && idObject.type !== `db_qualifier`)
		throw new Error(`Object with id ${qualifier.id} is not a structured name.`)

	// This distinction is necessary since the wizard assumes defining a new qualifier includes
	// defining a new name so the name is stored directly in the qualifier
	const qualifierName = idObject.type === `db_qualifier`
		? findId(state, qualifier.qualifier_name_id)
		: qualifier

	return qualifierName ? qualifierName.name : ``
}

const formatStructuredName = (structuredName, state) => {
	const idObject = parseId(structuredName.id)
	if (idObject.type !== `structured_name` && idObject.type !== `db_structured_name`)
		throw new Error(`Object with id ${structuredName.id} is not a structured name.`)

	const name = findId(state, structuredName.name_id)
	const qualifierName = formatQualifier(findId(state, structuredName.qualifier_id), state)
	const location = findId(state,  structuredName.location_id)
	return `${name ? name.name : ``} / ${qualifierName} / ${location ? location.name : ``}`
}

const Sname = ({data}) => {
	const dispatch = useDispatch()
	const state = useSelector(v => v)
	const referenceData = state.ref
	const refs = referenceData.reduce((p, c) => p.concat(...c.names.map(v => {return {...v, refId: c.id}})), [])

	const names = refs.filter(v => v.variant === `name`)
		.concat(...loadServerData(`names`))
		.map(v => [v.id, v.name])

	const qualifiers = refs.filter(v => v.variant === `qualifier`)
		.concat(...loadServerData(`qualifiers`))
		.map(v => [v.id, formatQualifier(v, state)])

	const locations = refs.filter(v => v.variant === `location`)
		.concat(...loadServerData(`locations`))
		.map(v => [v.id, v.name])

	const references = referenceData
		.concat(...loadServerData(`references`))
		.map(v => [v.id, v.title])

	const update = ({target}, field) => {
		const r = {...data}
		r[field] = target.value
		dispatch(updateSname(r))
	}

	return (<div>
		<label htmlFor="name">Name</label>
		<Dropdown name="name"  options={names} value={data.name} onChange={e => update(e, `name_id`)} />
		<br />
		<label htmlFor="qualifier">Qualifier</label>
		<Dropdown name="qualifier"  options={qualifiers} value={data.qualifier} onChange={e => update(e, `qualifier_id`)} />
		<br />
		<label htmlFor="location">Location</label>
		<Dropdown name="location" options={locations} value = {data.location} onChange={e => update(e, `location_id`) } />
		<br />
		<label htmlFor="reference">Reference</label>
		<Dropdown name="reference" options={references} value = {data.reference_id} onChange={e => update(e, `reference_id`)} />
	</div>)
}

const Rel = ({data}) => {
	const dispatch = useDispatch()
	const state = useSelector(v => v)

	const name1Options = state.sname
		.concat(...loadServerData(`structured_names`))
		.filter(v => v.id !== data.name2)
		.map(v => [v.id, formatStructuredName(v, state)])

	const name2Options = state.sname
		.concat(...loadServerData(`structured_names`))
		.filter(v => v.id !== data.name1)
		.map(v => [v.id, formatStructuredName(v, state)])

	const update = ({target}, field) => {
		const r = {...data}
		r[field] = target.value
		dispatch(updateRel(r))
	}

	const refOptions = state.ref
		.concat(...loadServerData(`references`))
		.map(v => [v.id, v.title])

	return (<div>
		<label htmlFor="reference">Reference</label>
		<Dropdown name="reference" options={refOptions} value = {data.reference_id} onChange={e => update(e, `reference_id`)} />
		<br />
		<Dropdown options={name1Options} value={data.name1} onChange={e => update(e, `name1`)} />
		<br />
		<Dropdown options={name2Options} value={data.name2} onChange={e => update(e, `name2`)} />
	</div>)
}

const blankRef = () => { return {id: makeId(`reference`), first_author: ``, year: 0, title: ``, doi: ``, link: ``, exists: false, queried: false, names: []}}
const blankSname = () => { return {id: makeId(`structured_name`), name_id: -1, qualifier_id: -1, location_id: -1, reference_id: -1, remarks:`` }}
const blankRel = () => { return {id: makeId(`relation`), name1: -1, name2: -1, reference_id: -1} }

const App = () => {
	const state = useSelector(v => v)
	const dispatch = useDispatch()
	useEffect(() => {
		initServer()
		const serverData = loadServerData()
		const map = {}
		serverData.names.forEach(v => map[v.id] = v)
		serverData.locations.forEach(v => map[v.id] = v)
		serverData.qualifier_names.forEach(v => map[v.id] = v)
		serverData.qualifiers.forEach(v => map[v.id] = v)
		serverData.structured_names.forEach(v => map[v.id] = v)
		serverData.references.forEach(v => map[v.id] = v)
		dispatch(initMapvalues(map))
	}, [])

	const addNewRef = e => {
		const ref = blankRef()
		dispatch(addRef(ref))
	}

	const addSnameHandler = e => {
		const sname = blankSname()
		dispatch(addSname(sname))
	}

	const addRelHandler = e => {
		dispatch(addRel(blankRel()))
	}

	return (
		<>
			<div>
				<h2>References</h2>
				{ state.ref.map(data => <Ref {...{key: data.id, data}} />) }
				<button type="button" onClick={addNewRef}>Add new reference</button>
			</div>
			<div>
				<h2>Structured Names</h2>
				{ state.sname.map(data => <Sname {...{key: data.id, data}} />) }
				<button type="button" onClick={addSnameHandler}>Add new structured name</button>
			</div>
			<div>
				<h2>Relations</h2>
				{ state.rel.map(data => <Rel {...{key: data.id, data}} />) }
				<button type="button" onClick={addRelHandler}>Add new relation</button>
			</div>
		</>
	);
}

export default App