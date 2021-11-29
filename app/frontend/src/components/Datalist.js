import React from 'react'

export const Datalist = ({ name, options, value, onChange }) => {
	//console.log(options[0])
	return (
		<>
			<input type='text' list={name} value={value} onChange={onChange} />
			<datalist id={name} data-testid={`datalist-test-id-${name}`}>
				{options.map(tuple => (
					<option key={tuple[0]} value={tuple[1]} />
				))}
			</datalist>
		</>
	)
}
