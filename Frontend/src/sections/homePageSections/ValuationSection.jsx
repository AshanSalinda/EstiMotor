import React, { useState, useEffect } from 'react';
import { getPrediction, getMakeModelMapping } from '../../api/userApi';
import Input from '../../components/input';
import Button from '../../components/input/Button';
import Select from '../../components/input/Select';
import VehicleAdCard from '../../components/VehicleAdCard';
import { useAlert } from "../../context/AlertContext.jsx";
import selectItems from '../../data/selectItems.json'
import useDisplayValueAnimation from '../../hooks/useDisplayValueAnimation';
import useVehicleInputValidation from '../../hooks/validations/useVehicleInputValidation';


function ValuationSection() {
    const [ isValueLoading, setIsValueLoading ] = useState(false);
    const [ isMakeLoading, setIsMakeLoading ] = useState(false);
    const [ makeModelMap, setMakeModelMap ] = useState({});
    const [ makeList, setMakeList ] = useState([]);
    const [ modelList, setModelList ] = useState([]);
    const [ SimilarAds, setSimilarAds ] = useState([]);
    const { displayValue, animateCount } = useDisplayValueAnimation();

    const { getAttributes, handleSubmit } = useVehicleInputValidation();
    const { showAlert } = useAlert();

    const yearOptions = selectItems.year.map((year) => ({value: year, label: year}));
    const transmissionOptions = selectItems.transmission.map((transmission) => ({value: transmission, label: transmission}));
    const fuelTypeOptions = selectItems.fuelType.map((fuelType) => ({value: fuelType, label: fuelType}));

    const onSubmit = async (formData) => {
        setIsValueLoading(true);
        setSimilarAds([]); // Clear previous ads

        const payload = {
            make: formData.make,
            model: formData.model.value,
            category: formData.model.category,
            year: Number(formData.year.replace(',', '')),
            transmission: formData.transmission,
            fuelType: formData.fuelType,
            engineCapacity: Number(formData.engineCapacity.replace(',', '')),
            mileage: Number(formData.mileage.replace(',', '')),
        };

        const element = document.getElementById('display-value');
        element.classList.add('opacity-0', 'pointer-events-none');

        if(element.getBoundingClientRect().bottom >= window.innerHeight){
            element.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }

        let predictedValue = 0;
        let ads = [];
        
        try {
            const result = await getPrediction(payload);
            predictedValue = result?.predictedValue || 0;
            ads = result?.similarAds || [];
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

        if (ads.length > 0) {
            element.scrollIntoView({behavior: 'smooth', block: 'center'});
        }

        await animateCount(predictedValue);

        element.classList.add('animate-glow');
        element.classList.remove('animate-fadeIn');

        setSimilarAds(ads);
    };


    const handleMakeChange = (e) => {
        const makeValue = e?.target?.value;

        if (makeValue) {
            setModelList(makeModelMap[makeValue] || []);
        } else {
            setModelList([]);
        }
    };


    useEffect(() => {
        setIsMakeLoading(true);

        getMakeModelMapping()
            .then((mappings) => {
                const map = {};
                const makeOptions = mappings.map(mapping => {
                    map[mapping.make] = mapping.models.map(model => ({
                        label: model.name,
                        value: model.name,
                        category: model.category
                    }));
                    return { label: mapping.make, value: mapping.make };
                });
                console.log(map)
                setMakeModelMap(map);
                setMakeList(makeOptions);
            })
            .catch(error => showAlert(error, "apiError"))
            .finally(() => setIsMakeLoading(false));
    }, []);


    return (
        <div id='input-section' className='min-h-screen px-2 md:px-10 md:mt-40 lg:mt-28 onlyMd:min-h-fit'>
            <form onSubmit={handleSubmit(onSubmit)} className='flex mx-auto lg:w-fit flex-col items-center justify-center space-y-16 text-center bg-gradient-to-t from-[#000000] to-[#121212] rounded-xl md:rounded-2xl md:px-16 lg:px-16'>

                <h1 className='pt-20 text-center font-semibold text-gray-200 max-w-60 md:max-w-[26rem] text-2xl md:text-3xl'>Know Your Vehicle's Market Value Instantly</h1>

                <div className="grid w-[80vw] md:w-[36rem] grid-cols-1 gap-3 md:grid-cols-2 md:gap-x-4 md:gap-y-2">
                    <Select {...getAttributes("Manufacturer", "make", handleMakeChange)} options={makeList} isLoading={isMakeLoading} />
                    <Select {...getAttributes("Model")} options={modelList} isFullOptionRequired={true} />
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

            {/* Vehicle Ads Grid */}
            {SimilarAds.length > 0 && (
                <div id="ads-grid" className="w-full pt-16 pb-24 md:pb-28 lg:pb-32 lg:px-10 animate-expand">
                    <h2 className="text-2xl font-semibold text-gray-200 ml-2 mb-6">Similar Vehicle Ads</h2>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        {SimilarAds.map((ad, idx) => (
                            <VehicleAdCard key={idx} ad={ad} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    )
}

export default ValuationSection
