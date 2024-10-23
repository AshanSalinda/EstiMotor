import Step from './Step';

class DataCleaningStep extends Step {
    constructor() {
        super('Data Cleaning', 'Cleaning and preparing data for processing...');
    }

    cleanData() {
        this.log('Data cleaning in progress...');
        // Implement the actual cleaning logic
        setTimeout(() => this.complete(), 3000);
    }
}

export default DataCleaningStep;
