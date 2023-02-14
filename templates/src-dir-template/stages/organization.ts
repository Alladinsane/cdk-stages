import { ArnComponents, Lazy, Stage, StageProps, Tags, Token } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as costCenters from '../configuration/cost-centers';
import { RegionConfigs } from '../configuration/regions';
import { RegionConfigBase } from '../configuration/regions/region-base';


export interface OrganizationProps extends StageProps {
    readonly accountName: string;
    readonly dependencies?: string[];
}

export abstract class Organization extends Stage {
    // Input properties
    public readonly accountName: string;

    // Standard properties
    public readonly organizationArn: ArnComponents = {
        account: '', // Account Id
        region: '',
        resource: 'organization',
        resourceName: '', // Organization Id
        service: 'organizations'
    };
    public readonly organizationId: string = '';
    public readonly ous: string[] = [];
    public readonly regionConfig: RegionConfigBase;

    constructor(scope: Construct, id: string, props: OrganizationProps) {
        super(scope, id, props);

        this.accountName = props.accountName;
        this.regionConfig = RegionConfigs[this.region!]

        if (props.dependencies) {
            console.log('I have dpendencies!!!!!!11!!!!!!!!!111!!!111');
            console.log(props.dependencies);
            this.node.setContext('dependencies', props.dependencies);
        }

        this.addTag('account-name', this.accountName);
        this.addTag('organizational-units', Lazy.uncachedString({
            produce: (_) => {
                return this.ous.join('/');
            }
        }));

        // Cost center tags
        this.addTag('cost-center', 'uncategorized', undefined, ['aws:cdk:stack'], 1);
        this.addTag('cost-center', 'analytics', costCenters.analytics);
        this.addTag('cost-center', 'database', costCenters.database);
        this.addTag('cost-center', 'delivery', costCenters.delivery);
        this.addTag('cost-center', 'dev', costCenters.dev);
        this.addTag('cost-center', 'disaster-recovery', costCenters.disasterRecovery);
        this.addTag('cost-center', 'infrastructure', costCenters.infrastructure);
        this.addTag('cost-center', 'marketing', costCenters.marketing);
        this.addTag('cost-center', 'monitoring', costCenters.monitoring);
        this.addTag('cost-center', 'network', costCenters.network);
        this.addTag('cost-center', 'operations', costCenters.operations);
        this.addTag('cost-center', 'security', costCenters.security);
        
    }

    addTag(key: string, value: string, include?: string[], exclude?: string[], priority?: number): void {
        let processedInclude = include ?? [];
        let processedExclude = exclude ?? [];

        if (Token.isUnresolved(key) || Token.isUnresolved(value)) {
            processedExclude.push('aws:cdk:stack');
        }

        Tags.of(this).add(key, value, {
            excludeResourceTypes: processedExclude.length ? processedExclude : undefined,
            includeResourceTypes: processedInclude.length ? processedInclude : undefined,
            priority: priority
        });
    }
}
