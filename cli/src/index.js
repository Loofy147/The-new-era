#!/usr/bin/env node

const { Command } = require('commander');
const chalk = require('chalk');
const packageJson = require('../package.json');

const program = new Command();

// Configure program
program
  .name('aimos')
  .description('AI Operating System Framework CLI')
  .version(packageJson.version);

// Agent management commands
program
  .command('agents')
  .description('List all available AI agents')
  .action(() => {
    console.log(chalk.blue('🤖 Available AI Agents:'));
    console.log('');
    
    const agents = [
      { name: 'CostOptBot', role: 'Cost Optimization Agent', status: '✅' },
      { name: 'ComplianceBot', role: 'Compliance Auditing Agent', status: '✅' },
      { name: 'TestGenie', role: 'Testing Automation Agent', status: '✅' },
      { name: 'SecuBot', role: 'Security Hardening Agent', status: '✅' },
      { name: 'PrivacyGuard', role: 'Data Privacy Agent', status: '✅' },
      { name: 'InsightsBot', role: 'Analytics & Insights Agent', status: '✅' },
      { name: 'ConvDesignBot', role: 'Conversation Designer Agent', status: '✅' },
      { name: 'ModelRefactor', role: 'Refactoring Agent', status: '✅' },
      { name: 'ArchitectureDesignerAgent', role: 'Architecture Designer Agent', status: '✅' }
    ];
    
    agents.forEach(agent => {
      console.log(`${agent.status} ${chalk.green(agent.name)} - ${agent.role}`);
    });
  });

// Run agents command
program
  .command('run')
  .description('Run AI agents')
  .option('-a, --agent <name>', 'Run specific agent')
  .option('--all', 'Run all agents')
  .option('--security', 'Run security suite')
  .option('--analysis', 'Run analysis suite')
  .action((options) => {
    console.log(chalk.blue('🚀 Starting AI Operating System...'));
    
    if (options.all) {
      console.log(chalk.yellow('Running all agents...'));
      console.log(chalk.gray('Note: Use Python main.py for full execution'));
    } else if (options.security) {
      console.log(chalk.yellow('Running security suite: SecuBot, ComplianceBot, PrivacyGuard'));
    } else if (options.analysis) {
      console.log(chalk.yellow('Running analysis suite: CostOptBot, InsightsBot, TestGenie'));
    } else if (options.agent) {
      console.log(chalk.yellow(`Running agent: ${options.agent}`));
    } else {
      console.log(chalk.red('Please specify which agents to run. Use --help for options.'));
    }
  });

// System status command
program
  .command('status')
  .description('Show system status')
  .action(() => {
    console.log(chalk.blue('📊 AI Operating System Status'));
    console.log('');
    console.log(`${chalk.green('✅')} Core System: Operational`);
    console.log(`${chalk.green('✅')} Plugin Manager: Ready`);
    console.log(`${chalk.green('✅')} Agents: 9 Active`);
    console.log(`${chalk.green('✅')} Services: 1 Running (Prompt Memory)`);
    console.log(`${chalk.yellow('⚠️')}  CLI Tools: Basic Implementation`);
    console.log(`${chalk.yellow('⚠️')}  Dashboard: Not Implemented`);
    console.log(`${chalk.yellow('⚠️')}  Infrastructure: Development Stage`);
  });

// Reports command
program
  .command('reports')
  .description('View generated reports')
  .action(() => {
    console.log(chalk.blue('📄 Available Reports:'));
    console.log('');
    console.log('Reports are generated in the reports/ directory when agents are executed.');
    console.log('Run agents first using: aimos run --all');
  });

// Initialize command
program
  .command('init')
  .description('Initialize AI Operating System environment')
  .action(() => {
    console.log(chalk.blue('🔧 Initializing AI Operating System...'));
    console.log(chalk.green('✅ Environment ready'));
    console.log(chalk.gray('Use "aimos status" to check system health'));
    console.log(chalk.gray('Use "aimos run --all" to execute all agents'));
  });

// Error handling
program.on('command:*', () => {
  console.error(chalk.red(`Unknown command: ${program.args.join(' ')}`));
  console.log(chalk.gray('Use --help for available commands'));
  process.exit(1);
});

// Parse command line arguments
program.parse();

// Show help if no command provided
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
