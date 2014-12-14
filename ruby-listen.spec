#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	listen
Summary:	Listen to file modifications
Name:		ruby-%{pkgname}
Version:	2.7.11
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	https://github.com/guard/listen/archive/v%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	2b1378df84cd0e5ab94d172c3a92d70d
Patch0:		deps.patch
URL:		https://github.com/guard/listen
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
%if %{with tests}
BuildRequires:	ruby-bundler >= 1.3.5
BuildRequires:	ruby-rake
BuildRequires:	ruby-rspec >= 2.14
BuildRequires:	ruby-rspec-retry
%endif
Requires:	ruby-celluloid >= 0.15.2
Requires:	ruby-celluloid-io >= 0.15.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Listen gem listens to file modifications and notifies you about
the changes. Works everywhere!

%prep
%setup -q -n %{pkgname}-%{version}
%patch0 -p1

%build
# make gemspec self-contained
ruby -r rubygems -e 'spec = eval(File.read("%{pkgname}.gemspec"))
	File.open("%{pkgname}-%{version}.gemspec", "w") do |file|
	file.puts spec.to_ruby_for_cache
end'

%if %{with tests}
rspec spec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md CHANGELOG.md
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
