import { Tags } from 'aws-cdk-lib';
import { Construct } from 'constructs';

/**
 * Configuration for the Environment Config
 */
export interface EnvironmentProps {
    /**
     * Name for the environment
     */
    readonly name: string;
    
    // Additional props unique to the environment
    
}

export class Environment extends Construct {
    // Input properties
    public readonly name: string;

    // Environment Properties
    constructor(scope: Construct, id: string, props: EnvironmentProps) {
        super(scope, id);

        this.name = props.name;
        
        Tags.of(this).add('environment', this.name)

        // Stacks that make up an environment
    }
    
}
