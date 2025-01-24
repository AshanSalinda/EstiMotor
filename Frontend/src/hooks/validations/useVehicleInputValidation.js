import { useForm } from "react-hook-form";


const useVehicleInputValidation = () => {
    const { register, handleSubmit, formState: { errors } } = useForm();

    /**
    * Generates form input attributes for React Hook Form.
    * 
    * @param {string}
    *    - `label`: The label text for the input field.
    *    - `name` : The name of the input field (optional). If not provided, it's derived from the label.
    * @returns {object} The attributes to spread on the input component, including:
    *    - `name`: Field name (camelCase version of label).
    *    - `onBlur`: Validation trigger for blur event.
    *    - `onChange`: Handles input changes.
    *    - `ref`: Reference for input element.
    *    - `helperText`: Error message (if any).
    *    - `error`: Boolean indicating if there's a validation error.
    *    - `label`: Original label text displayed as the input label.
    * 
    * @example
    * const { getAttributes } = useVehicleInputValidation();
    * <Input {...getAttributes("Engine Capacity")} />
    */
    const getAttributes = (label, name, customChangeHandler) => {

        if (!name) {
            name = label.charAt(0).toLowerCase() + label.slice(1).replace(/\s+/g, '');
        }

        const { onChange : registerChangeHandler, ...rest } = register(name, { required: `${label} is Required.` });

        const combinedChangeHandler = (e) => { 
            registerChangeHandler(e); 
            
            if (typeof(customChangeHandler) === 'function'){
                customChangeHandler(e);
            }
        };

        return {
            ...rest,
            onChange: combinedChangeHandler,
            helperText: errors?.[name]?.message,
            error: !!errors?.[name],
            label,
        };
    };

    return { getAttributes, handleSubmit };
};

export default useVehicleInputValidation;