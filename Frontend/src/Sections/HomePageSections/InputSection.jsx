import React, { useState, useEffect } from 'react';
import Input from '../../components/input';
import Button from '../../components/input/Button';
import Select from '../../components/input/Select';
import selectItems from '../../data/selectItems.json'
import useDisplayValueAnimation from '../../hooks/useDisplayValueAnimation';
import useVehicleInputValidation from '../../hooks/validations/useVehicleInputValidation';
import { getPrediction, getMakeList, getModelList } from '../../api/userApi';
import { useAlert } from "../../context/AlertContext.jsx";

function InputSection() {
    const [ isValueLoading, setIsValueLoading ] = useState(false);
    const [ isMakeLoading, setIsMakeLoading ] = useState(false);
    const [ isModelLoading, setIsModelLoading ] = useState(false);
    const [ makeList, setMakeList ] = useState([]);
    const [ modelList, setModelList ] = useState([]);
    const { displayValue, animateCount } = useDisplayValueAnimation();

    const { getAttributes, handleSubmit } = useVehicleInputValidation();
    const { showAlert } = useAlert();

    const yearOptions = selectItems.year.map((year) => ({value: year, label: year}));
    const transmissionOptions = selectItems.transmission.map((transmission) => ({value: transmission, label: transmission}));
    const fuelTypeOptions = selectItems.fuelType.map((fuelType) => ({value: fuelType, label: fuelType}));

    const onSubmit = async (formData) => {
        setIsValueLoading(true);

        const payload = {
            make: formData.make,
            model: formData.model,
            year: Number(formData.year.replace(',', '')),
            transmission: formData.transmission,
            fuelType: formData.fuelType,
            engineCapacity: Number(formData.engineCapacity.replace(',', '')),
            mileage: Number(formData.mileage.replace(',', '')),
        };

        console.log(formData)
        console.log(payload)

        const element = document.getElementById('display-value');
        element.classList.add('opacity-0', 'pointer-events-none');

        if(element.getBoundingClientRect().bottom >= window.innerHeight){
            element.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }

        let predictedValue = 0;
        try {
            predictedValue = await getPrediction(payload);
        }
        catch(error) {
            showAlert(error, "apiError")
            return;
        }
        finally {
            setIsValueLoading(false);
        }

        element.classList.remove('opacity-0', 'pointer-events-none', 'animate-glow');
        element.classList.add('animate-fadeIn');

        await animateCount(predictedValue);

        element.classList.add('animate-glow');
        element.classList.remove('animate-fadeIn');
    };


    const handleMakeChange = (e) => {
        if (e?.target?.value) {
            setIsModelLoading(true);
            setModelList([]);

            getModelList(e?.target?.value)
                .then((modelList) => setModelList(modelList))
                .finally(() => setIsModelLoading(false));
        } else {
            setModelList([]);
        }
    };


    useEffect(() => {
        setIsMakeLoading(true);

        getMakeList()
            .then((makeList) => setMakeList(makeList))
            .finally(() => setIsMakeLoading(false));
    }, []);


    return (
        <div id='input-section' className='flex justify-center min-h-screen px-2 md:px-10 md:mt-40 lg:mt-28 onlyMd:min-h-fit'>
            <form onSubmit={handleSubmit(onSubmit)} className='flex lg:min-w-[48vw] flex-col items-center justify-center space-y-16 text-center bg-gradient-to-t from-[#000000] to-[#121212] rounded-2xl md:rounded-3xl md:px-16 lg:px-16'>

                <h1 className='px-10 pt-20 text-3xl font-semibold text-gray-200 max-w-[32rem] md:text-3xl'>Know Your Vehicle's Market Value Instantly</h1>

                <div className="grid w-[85vw] md:w-fit grid-cols-1 gap-3 md:grid-cols-2 md:gap-x-4 md:gap-y-2 lg:w-[36rem]">
                    <Select {...getAttributes("Manufacturer", "make", handleMakeChange)} options={makeList} isLoading={isMakeLoading} />
                    <Select {...getAttributes("Model")} options={modelList} isLoading={isModelLoading} />
                    <Select {...getAttributes("Make Year", "year")} options={yearOptions} />
                    <Select {...getAttributes("Transmission")} options={transmissionOptions} />
                    <Select {...getAttributes("Fuel Type")} options={fuelTypeOptions} />
                    <Input {...getAttributes("Engine Capacity")} ending="CC" type="number" autoComplete='off'  />
                    <Input {...getAttributes("Mileage")} ending="KM" type="number" autoComplete='off' />
                </div>

                <Button
                    label="Get Value"
                    size="medium"
                    type="submit"
                    sx={{ width: "10rem", borderRadius: "1.3rem" }}
                />


                <div className='relative'>
                    { isValueLoading &&
                        <div className="absolute flex items-center justify-center w-full h-10 space-x-2">
                            <div className="w-3 h-3 bg-gray-500 rounded-full animate-[bounce_1.5s_ease-in-out_infinite]"></div>
                            <div className="w-3 h-3 bg-gray-500 rounded-full animate-[bounce_1.5s_ease-in-out_200ms_infinite]"></div>
                            <div className="w-3 h-3 bg-gray-500 rounded-full animate-[bounce_1.5s_ease-in-out_400ms_infinite]"></div>
                        </div>
                    }
                    
                    <p id='display-value' className="pb-16 text-3xl font-medium tracking-tight opacity-0 pointer-events-none text-slate-100 md:text-4xl tabular-nums font-monoSpace">
                        {`LKR ${displayValue}`}
                    </p>
                </div>

            </form>
        </div>
    )
}

export default InputSection