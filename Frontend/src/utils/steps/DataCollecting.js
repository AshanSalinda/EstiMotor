import Step from './Step';

class DataCollectingStep extends Step {
    constructor() {
        super('Data Collecting', 'Collecting data from various sources...');
    }

    collectData() {
        // this.log('Data collection has begun.');
        // Simulate the process or actual logic
        setTimeout(() => this.complete(), 2000); // Automatically mark it as complete after 2 seconds
    }
}

export default DataCollectingStep;
